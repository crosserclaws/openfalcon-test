package main

import (
	"database/sql"
	"flag"
	"fmt"
	"log"
	"reflect"
	"runtime"

	_ "github.com/go-sql-driver/mysql"
)

const (
	Error int64 = -1
	Empty int64 = 0
)

var (
	Debug    bool
	DbAddr   string
	DbConfig string = "?charset=utf8&loc=Asia%2FTaipei"

	testAgent string = "fake-agent"
	userList         = []User{
		{"fakeuser1", "070424e5398ec581c27100a0d63fc86e", ""},
		{"fakeuser2", "070424e5398ec581c27100a0d63fc86e", "cheminlin@cepave.com"},
	}

	gIndex int
)

type User struct {
	Name   string
	Passwd string
	Email  string
}

func main() {
	// Parse cmd-line flags
	var ip, mode string
	flag.BoolVar(&Debug, "debug", false, "Debugging msg.")
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
	fmt.Println("[BUILD]")
	buildUic()
	buildPortal()
}

func clean() {
	fmt.Println("[CLEAN]")
	cleanUic()
	cleanPortal()
}

/*
 *
 * Utility functions
 *
 */

// SELECT before INSERT; return id.
// Use callback if SELECT do not retrieve any data.
func InsertSelectId(
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
		if id == Error {
			PrintMsg(2, "FAIL!", fnName)
		} else {
			PrintMsg(2, "PASS.", fnName)
		}
	case err != nil:
		id = Error
		PrintCheckErr(4, err)
		PrintMsg(2, "FAIL!", fnName)
	default:
		printDebug(3, "SELECT_ID =", id)
		PrintMsg(2, "PASS.", fnName)
	}
	return id
}

// SELECT before DELETE; return id.
// If @selectColName is an empty string, DELETE without SELECT.
func DeleteSelectId(
	db *sql.DB,
	selectColName string,
	querySuffix string, args ...interface{},
) int64 {
	var id int64
	if selectColName != "" {
		sqlQuery := "SELECT " + selectColName + " " + querySuffix
		row := db.QueryRow(
			sqlQuery, args...,
		)

		err := row.Scan(&id)
		switch {
		case err == sql.ErrNoRows:
			printDebug(3, "No need to clean:", args)
			return Empty
		case err != nil:
			PrintCheckErr(4, err)
			PrintMsg(2, "FAIL!", args)
			return Error
		default:
			printDebug(3, "SELECT_ID =", id)
		}
	}

	sqlQuery := "DELETE " + querySuffix
	affect := DeleteExec(db, sqlQuery, args...)
	if affect == Empty {
		PrintMsg(2, "WARN?", "Clean nothing:", args)
	} else if affect == Error {
		PrintMsg(2, "FAIL!", args)
	} else {
		PrintMsg(2, "PASS.", args)
	}
	return id
}

func InsertExec(db *sql.DB, sqlQuery string, args ...interface{}) int64 {
	res, err := db.Exec(sqlQuery, args...)
	return HandleRes(res.LastInsertId, err)
}

func DeleteExec(db *sql.DB, sqlQuery string, args ...interface{}) int64 {
	res, err := db.Exec(sqlQuery, args...)
	return HandleRes(res.RowsAffected, err)
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

// IoC callback to handle sql.Result.
func HandleRes(callback func() (int64, error), err error) int64 {
	if err != nil {
		PrintErr(4, err)
	} else {
		id, err := callback()
		if err != nil {
			PrintErr(4, err)
		} else {
			return id
		}
	}
	return Error
}

/*
 *
 * Build functions
 *
 */

var (
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
		uid = InsertSelectId(db, insertUser,
			"SELECT id FROM user WHERE name=?", u.Name)
		uids = append(uids, uid)
	}

	tid = InsertSelectId(db, insertTeam,
		"SELECT id from team WHERE name=?",
		"fake_user_group")

	for gIndex, u = range userList {
		_ = InsertSelectId(db, insertRelTeamUser,
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

	aid = InsertSelectId(db, insertAction, "SELECT id FROM action WHERE uic=?", "fake_user_group")
	hid = InsertSelectId(db, insertHost, "SELECT id FROM host WHERE hostname=?", testAgent)
	gid = InsertSelectId(db, insertGrp, "SELECT id FROM grp WHERE grp_name=?", "fake_host_group")
	tpid = InsertSelectId(db, insertTpl, "SELECT id FROM tpl WHERE tpl_name=?", "fake_template")
	sid = InsertSelectId(db, insertStrategy, "SELECT id FROM strategy WHERE tpl_id=?", tpid)
	_ = InsertSelectId(db, insertGrpHost, "SELECT grp_id FROM grp_host WHERE grp_id=? AND host_id=?", gid, hid)
	_ = InsertSelectId(db, insertGrpTpl, "SELECT grp_id FROM grp_tpl WHERE grp_id=? AND tpl_id=?", gid, tpid)
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

/*
 *
 * Clean functions
 *
 */

var (
	cUids []int64
	cUid  int64
	cTid  int64

	cAid  int64
	cHid  int64
	cGid  int64
	cTpid int64
	cSid  int64
)

func cleanUic() {
	db := DbConnect("uic")
	defer db.Close()

	var u User
	for gIndex, u = range userList {
		cUid = DeleteSelectId(db, "id",
			"FROM user WHERE name=?", u.Name)
		cUids = append(cUids, cUid)
	}

	cTid = DeleteSelectId(db, "id",
		"FROM team WHERE name=?",
		"fake_user_group")

	for gIndex, u = range userList {
		_ = DeleteSelectId(db, "",
			"FROM rel_team_user WHERE tid=? AND uid=?",
			cTid, cUids[gIndex])
	}
}

func cleanPortal() {
	db := DbConnect("falcon_portal")
	defer db.Close()

	cAid = DeleteSelectId(db, "id", "FROM action WHERE uic=?", "fake_user_group")
	cHid = DeleteSelectId(db, "id", "FROM host WHERE hostname=?", testAgent)
	cGid = DeleteSelectId(db, "id", "FROM grp WHERE grp_name=?", "fake_host_group")
	cTpid = DeleteSelectId(db, "id", "FROM tpl WHERE tpl_name=?", "fake_template")
	cSid = DeleteSelectId(db, "id", "FROM strategy WHERE tpl_id=?", cTpid)
	_ = DeleteSelectId(db, "", "FROM grp_host WHERE grp_id=? AND host_id=?", cGid, cHid)
	_ = DeleteSelectId(db, "", "FROM grp_tpl WHERE grp_id=? AND tpl_id=?", cGid, cTpid)
}
