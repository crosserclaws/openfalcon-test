package main

import (
	"database/sql"
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

	testID    int    = 7777
	testAgent string = "test-agent"
	timeStamp string = time.Now().Format("2006-01-02 15:04:05")
	userList         = []User{
		{1, "root", "070424e5398ec581c27100a0d63fc86e", "", 2},
		{testID, "cheminlin", "a5b8fedaf75e5396b3ae2c6e60b55da6", "cheminlin@cepave.com", 2},
	}
)

type User struct {
	Id     int
	Name   string
	Passwd string
	Email  string
	Role   int
}

type DbFlow struct {
	DbName string
	FnList []FnFlow
}

type FnFlow func(*sql.DB) []error

func main() {

	var dbList = []DbFlow{
		{"falcon_portal", []FnFlow{initTbAction, initTbHost, initTbTpl, initTbStrategy, initTbGrp, initTbGrpHost, initTbGrpTpl}},
		{"uic", []FnFlow{initTbUser, initTbTeam, initTbRelTeamUser}},
	}

	for _, flow := range dbList {
		runDbFlow(flow)
	}
}

func runDbFlow(flow DbFlow) {
	// Connect to a DB
	dbName := dbAddr + flow.DbName + dbConfig
	db, err := sql.Open("mysql", dbName)
	if err != nil {
		log.Fatalf("[Addr=%s] %v\n", dbName, err)
	}
	defer db.Close()

	for _, ff := range flow.FnList {
		fnName := runtime.FuncForPC(reflect.ValueOf(ff).Pointer()).Name()
		passFlag := true
		errList := ff(db)
		for _, err := range errList {
			if err != nil {
				fmt.Printf("[Db=%s][Fn=%s] %v\n", flow.DbName, fnName, err)
				passFlag = false
			}
		}
		if passFlag {
			fmt.Printf("[Db=%s][Fn=%s] Pass.\n", flow.DbName, fnName)
		}
	}
}

func initTbAction(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO action (id, uic, url, callback, before_callback_sms, before_callback_mail, after_callback_sms, after_callback_mail) 
		VALUES (?, 'test_user_group', '', 0, 0, 0, 0, 0)
		`, testID+int('a'))
	return []error{err}
}

func initTbHost(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO host (id, hostname, ip, agent_version, plugin_version, maintain_begin, maintain_end, update_at)
		VALUES (?, ?, '10.20.30.40', '0.0.1', 'plugin not enabled', 0, 0, ?)
		`, testID+int('h'), testAgent, timeStamp)
	return []error{err}
}

func initTbGrp(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO grp (id, grp_name, create_user, create_at, come_from)
		VALUES (?, 'test_host_group', 'root', ?, 1)
		`, testID+int('g'), timeStamp)
	return []error{err}
}

func initTbGrpHost(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO grp_host (grp_id, host_id)
		VALUES (?, ?)
		`, testID+int('g'), testID+int('h'))
	return []error{err}
}

func initTbGrpTpl(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO grp_tpl (grp_id, tpl_id, bind_user)
		VALUES (?, ?, 'root')
		`, testID+int('g'), testID+int('t'))
	return []error{err}
}

func initTbTpl(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO tpl (id, tpl_name, parent_id, action_id, create_user, create_at)
		VALUES (?, 'test_template', 0, ?, 'root', ?)
		`, testID+int('t'), testID+int('a'), timeStamp)
	return []error{err}
}

func initTbStrategy(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO strategy (id, metric, tags, max_step, priority, func, op, right_value, note, run_begin, run_end, tpl_id)
		VALUES (?, 'cpu.idle', '', 3, 0, 'all(#2)', '<=', 100, '', '', '', ?)
		`, testID+int('s'), testID+int('t'))
	return []error{err}
}

func initTbRelTeamUser(db *sql.DB) []error {
	errList := []error{}
	for k, v := range userList {
		_, err := db.Exec(
			`
			INSERT INTO rel_team_user (id, tid, uid)
			VALUES (?, ?, ?)
			`, testID+k, testID, v.Id)
		errList = append(errList, err)
	}
	return errList
}

func initTbTeam(db *sql.DB) []error {
	_, err := db.Exec(
		`
		INSERT INTO team(id, name, resume, creator, created)
		VALUES (?, "test_user_group", "", 1, ?)
		`, testID, timeStamp)
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
