package main

import (
	"database/sql"
	"flag"
	"fmt"
	"log"
	"reflect"
	"runtime"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

const (
	Empty int64 = -1
)

var (
	Debug    bool
	DbAddr   string
	DbConfig string = "?charset=utf8&loc=Asia%2FTaipei"

	testIdBase int    = 7777
	testIdLast int    = testIdBase + int('z')
	testAgent  string = "test-agent"
	timeStamp  string = time.Now().Format("2006-01-02 15:04:05")
	userList          = []User{
		{"fakeuser1", "070424e5398ec581c27100a0d63fc86e", ""},
		{"fakeuser2", "070424e5398ec581c27100a0d63fc86e", "cheminlin@cepave.com"},
	}
)

type User struct {
	Name   string
	Passwd string
	Email  string
}

type DbCase struct {
	DbName string
	FnFlow []FnVar
}

type FnVar func(*sql.DB) []error

func main() {
	// Parse cmd-line flags
	var ip, mode string
	flag.BoolVar(&Debug, "debug", false, "Debugging or not.")
	flag.StringVar(&ip, "ip", "10.20.30.40", "MySQL IP address.")
	flag.StringVar(&mode, "mode", "",
		"[cab | clean | build]\n\t"+
			"build  - Build data. (DB must be clean before build if DB is not empty.)\n\t"+
			"cab    - Clean & Build.\n\t"+
			"clean  - Clean data.\n\t")
	flag.Parse()
	DbAddr = fmt.Sprintf("root:password@tcp(%s:3306)/", ip)

	switch mode {
	case "cab":
		clean()
		build()
	case "clean":
		clean()
	case "build":
		build()
	default:
		flag.Usage()
	}
	// :~)

}

func build() {

	buildUic()
	buildPortal()

}

// IoC Callback for id
// This method would use sql.DB.QueryRow method to retrive data
func QueryForId(
	db *sql.DB,
	callback func(db *sql.DB) int64,
	sqlQuery string, args ...interface{},
) int64 {
	var id int64
	fnName := runtime.FuncForPC(reflect.ValueOf(callback).Pointer()).Name()
	row := db.QueryRow(
		sqlQuery, args...,
	)

	err := row.Scan(&id)
	switch {
	case err == sql.ErrNoRows:
		id = callback(db)
		printDebug(3, "INSERT_ID =", id)
		if id == Empty {
			PrintMsg(2, "FAIL!", fnName)
		} else {
			PrintMsg(2, "PASS.", fnName)
		}
	case err != nil:
		PrintCheckErr(4, err)
		PrintMsg(2, "FAIL!", fnName)
	default:
		printDebug(3, "SELECT_ID =", id)
		PrintMsg(2, "PASS.", fnName)
	}
	return id
}

func InsertExec(db *sql.DB, sqlQuery string, args ...interface{}) int64 {
	return HandleRes(db.Exec(sqlQuery, args...))
}

func DbConnect(dbName string) *sql.DB {
	dbSrc := DbAddr + dbName + DbConfig
	db, err := sql.Open("mysql", dbSrc)
	if err != nil {
		log.Fatalf("[Src=%s] %v\n", dbSrc, err)
	}
	return db
}

func PrintCheckErr(skip int, err error) {
	if err != nil {
		PrintErr(skip, err)
	}
}

func PrintErr(skip int, err error) {
	PrintMsg(skip, "ERROR", err)
}

func printDebug(skip int, args ...interface{}) {
	if Debug {
		PrintMsg(skip, "DEBUG", args...)
	}
}

func PrintMsg(skip int, prefix string, args ...interface{}) {
	pc, _, line, _ := runtime.Caller(skip)
	fmt.Printf("[%s][%s:%v] ", prefix, runtime.FuncForPC(pc).Name(), line)
	fmt.Println(args...)
}

func HandleRes(res sql.Result, err error) int64 {
	if err != nil {
		PrintErr(4, err)
	} else {
		id, err := res.LastInsertId()
		if err != nil {
			PrintErr(4, err)
		} else {
			return id
		}
	}
	return Empty
}

var (
	gIndex     int
	createUser string = userList[0].Name

	uids []int64
	uid  int64
	tid  int64

	aid  int64
	hid  int64
	gid  int64
	tpid int64
	sid  int64
)

func buildUic() {
	db := DbConnect("uic")
	defer db.Close()

	var u User
	for gIndex, u = range userList {
		uid = QueryForId(db, insertUser,
			"SELECT id FROM user WHERE name=?", u.Name)
		uids = append(uids, uid)
	}

	tid = QueryForId(db, insertTeam,
		"SELECT id from team WHERE name=?",
		"fake_user_group")

	for gIndex, u = range userList {
		_ = QueryForId(db, insertRelTeamUser,
			"SELECT id from rel_team_user WHERE tid=? AND uid=?",
			tid, uids[gIndex])
	}
}

func insertUser(db *sql.DB) int64 {
	u := userList[gIndex]
	return InsertExec(db,
		`INSERT INTO user(name ,passwd, email, role, creator, created)
		VALUES (?, ?, ?, 2, 0, "2016-01-01 01:01:01")`, u.Name, u.Passwd, u.Email)
}

func insertTeam(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO team(name, resume, creator, created) 
		VALUES ("fake_user_group", "", ?, "2016-01-01 01:01:01")`, uid)
}

func insertRelTeamUser(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO rel_team_user (tid, uid)
		VALUES (?, ?)`, tid, uids[gIndex])
}

func buildPortal() {
	db := DbConnect("falcon_portal")
	defer db.Close()

	aid = QueryForId(db, insertAction, "SELECT id FROM action WHERE uic=?", "fake_user_group")
	hid = QueryForId(db, insertHost, "SELECT id FROM  host WHERE hostname=?", testAgent)
	gid = QueryForId(db, insertGrp, "SELECT id FROM grp WHERE grp_name=?", "fake_host_group")
	tpid = QueryForId(db, insertTpl, "SELECT id FROM tpl WHERE tpl_name=?", "fake_template")
	sid = QueryForId(db, insertStrategy, "SELECT id FROM strategy WHERE tpl_id=?", tpid)
	_ = QueryForId(db, insertGrpHost, "SELECT grp_id FROM grp_host WHERE grp_id=? AND host_id=?", gid, hid)
	_ = QueryForId(db, insertGrpTpl, "SELECT grp_id FROM grp_tpl WHERE grp_id=? AND tpl_id=?", gid, tpid)

}

func insertAction(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO action (uic, url, callback, before_callback_sms, before_callback_mail, after_callback_sms, after_callback_mail) 
		VALUES ("fake_user_group", "", 0, 0, 0, 0, 0)`)
}

func insertHost(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO host (hostname, ip, agent_version, plugin_version, maintain_begin, maintain_end, update_at)
		VALUES (?, '10.20.30.40', '0.0.1', 'plugin not enabled', 0, 0, "2016-01-01 01:01:01")
		`, testAgent)
}

func insertGrp(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO grp (grp_name, create_user, create_at, come_from)
		VALUES ("fake_host_group", ?, "2016-01-01 01:01:01", 1)`, createUser)
}

func insertTpl(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO tpl (tpl_name, parent_id, action_id, create_user, create_at)
		VALUES ("fake_template", 0, ?, ?, "2016-01-01 01:01:01")`, aid, createUser)
}

func insertStrategy(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO strategy (metric, tags, max_step, priority, func, op, right_value, note, run_begin, run_end, tpl_id)
		VALUES ("cpu.idle", "", 3, 0, "all(#2)", "<=", 100, "", "", "", ?)
		`, tpid)
}

func insertGrpHost(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO grp_host (grp_id, host_id)
		VALUES (?, ?)`, gid, hid)
}

func insertGrpTpl(db *sql.DB) int64 {
	return InsertExec(db,
		`INSERT INTO grp_tpl (grp_id, tpl_id, bind_user)
		VALUES (?, ?, ?)
		`, gid, tpid, createUser)
}

func clean() {
	cleanDb("uic", "id", "user", "team", "rel_team_user")
	cleanDb("falcon_portal", "id", "action", "grp", "host", "strategy", "tpl")
	cleanDb("falcon_portal", "grp_id", "grp_host", "grp_tpl")
}

func cleanDb(dbName string, colName string, tabNames ...string) {
	db := DbConnect(dbName)
	defer db.Close()

	for _, tab := range tabNames {
		passFlag := true
		errList := cleanTabById(db, tab, colName)
		for _, err := range errList {
			if err != nil {
				fmt.Printf("[Db=%s][Tb=%s] %v\n", dbName, tab, err)
				passFlag = false
			}
		}
		if passFlag {
			fmt.Printf("[Db=%s][Tb=%s] Pass.\n", dbName, tab)
		}
	}
}

func cleanTabById(db *sql.DB, tabName string, colName string) []error {
	errList := []error{}
	stmt := fmt.Sprintf("DELETE FROM %s WHERE %s=?", tabName, colName)
	for i := testIdBase; i <= testIdLast; i++ {
		_, err := db.Exec(stmt, i)
		errList = append(errList, err)
	}
	return errList
}
