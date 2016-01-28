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

var (
	dbAddr   string = "root:password@tcp(10.20.30.40:3306)/"
	dbConfig string = "?charset=utf8&loc=Asia%2FTaipei"

	testIdBase int    = 7777
	testIdLast int    = testIdBase + int('z')
	testAgent  string = "test-agent"
	timeStamp  string = time.Now().Format("2006-01-02 15:04:05")
	userList          = []User{
		{1, "root", "070424e5398ec581c27100a0d63fc86e", "", 2},
		{testIdBase, "cheminlin", "a5b8fedaf75e5396b3ae2c6e60b55da6", "cheminlin@cepave.com", 2},
	}
)

type User struct {
	Id     int
	Name   string
	Passwd string
	Email  string
	Role   int
}

type DbCase struct {
	DbName string
	FnFlow []FnVar
}

type FnVar func(*sql.DB) []error

func main() {
	// Parse cmd-line flags
	var mode string
	flag.StringVar(&mode, "mode", "",
		"[cab | clean | build]\n\t"+
			"build  - Build data. (DB must be clean before build if DB is not empty.)\n\t"+
			"cab    - Clean & Build.\n\t"+
			"clean  - Clean data.\n\t")
	flag.Parse()

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
	var dbSuite = []DbCase{
		{"falcon_portal", []FnVar{initTbAction, initTbHost, initTbTpl, initTbStrategy, initTbGrp, initTbGrpHost, initTbGrpTpl}},
		{"uic", []FnVar{initTbUser, initTbTeam, initTbRelTeamUser}},
	}

	for _, dc := range dbSuite {
		runDbFlow(dc)
	}
}

func clean() {
	cleanDb("uic", "id", "user", "team", "rel_team_user")
	cleanDb("falcon_portal", "id", "action", "grp", "host", "strategy", "tpl")
	cleanDb("falcon_portal", "grp_id", "grp_host", "grp_tpl")
}

func cleanDb(dbName string, colName string, tabNames ...string) {
	db := dbConnect(dbName)
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

func runDbFlow(dc DbCase) {
	db := dbConnect(dc.DbName)
	defer db.Close()

	for _, ff := range dc.FnFlow {
		fnName := runtime.FuncForPC(reflect.ValueOf(ff).Pointer()).Name()
		passFlag := true
		errList := ff(db)
		for _, err := range errList {
			if err != nil {
				fmt.Printf("[Db=%s][Fn=%s] %v\n", dc.DbName, fnName, err)
				passFlag = false
			}
		}
		if passFlag {
			fmt.Printf("[Db=%s][Fn=%s] Pass.\n", dc.DbName, fnName)
		}
	}
}

func dbConnect(dbName string) *sql.DB {
	dbSrc := dbAddr + dbName + dbConfig
	db, err := sql.Open("mysql", dbSrc)
	if err != nil {
		log.Fatalf("[Src=%s] %v\n", dbSrc, err)
	}
	return db
}

func initTbAction(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO action (id, uic, url, callback, before_callback_sms, before_callback_mail, after_callback_sms, after_callback_mail) 
		VALUES (?, 'test_user_group', '', 0, 0, 0, 0, 0)
		`, testIdBase+int('a'))
	return []error{err}
}

func initTbHost(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO host (id, hostname, ip, agent_version, plugin_version, maintain_begin, maintain_end, update_at)
		VALUES (?, ?, '10.20.30.40', '0.0.1', 'plugin not enabled', 0, 0, ?)
		`, testIdBase+int('h'), testAgent, timeStamp)
	return []error{err}
}

func initTbGrp(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO grp (id, grp_name, create_user, create_at, come_from)
		VALUES (?, 'test_host_group', 'root', ?, 1)
		`, testIdBase+int('g'), timeStamp)
	return []error{err}
}

func initTbGrpHost(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO grp_host (grp_id, host_id)
		VALUES (?, ?)
		`, testIdBase+int('g'), testIdBase+int('h'))
	return []error{err}
}

func initTbGrpTpl(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO grp_tpl (grp_id, tpl_id, bind_user)
		VALUES (?, ?, 'root')
		`, testIdBase+int('g'), testIdBase+int('t'))
	return []error{err}
}

func initTbTpl(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO tpl (id, tpl_name, parent_id, action_id, create_user, create_at)
		VALUES (?, 'test_template', 0, ?, 'root', ?)
		`, testIdBase+int('t'), testIdBase+int('a'), timeStamp)
	return []error{err}
}

func initTbStrategy(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO strategy (id, metric, tags, max_step, priority, func, op, right_value, note, run_begin, run_end, tpl_id)
		VALUES (?, 'cpu.idle', '', 3, 0, 'all(#2)', '<=', 100, '', '', '', ?)
		`, testIdBase+int('s'), testIdBase+int('t'))
	return []error{err}
}

func initTbRelTeamUser(db *sql.DB) []error {
	errList := []error{}
	for k, v := range userList {
		_, err := db.Exec(
			`
			INSERT INTO rel_team_user (id, tid, uid)
			VALUES (?, ?, ?)
			`, testIdBase+k, testIdBase, v.Id)
		errList = append(errList, err)
	}
	return errList
}

func initTbTeam(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO team(id, name, resume, creator, created)
		VALUES (?, "test_user_group", "", 1, ?)
		`, testIdBase, timeStamp)
	return []error{err}
}

func initTbUser(db *sql.DB) []error {
	errList := []error{}
	for _, v := range userList {
		_, err := db.Exec(
			`
				INSERT INTO user(id, name ,passwd, email, role, creator, created) 
				VALUES (?, ?, ?, ?, ?, 0, ?)
				`, v.Id, v.Name, v.Passwd, v.Email, v.Role, timeStamp)
		errList = append(errList, err)
	}
	return errList
}
