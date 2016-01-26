package main

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var (
	agentConfig string = "agent.json"
	judgeConfig string = "judge.json"
	dbAddr      string = "root:password@tcp(10.20.30.40:3306)/"
	dbConfig    string = "?charset=utf8&loc=Asia%2FTaipei"

	testID    int    = 7777
	testAgent string = "test-agent"
	timeStamp string = time.Now().Format("2006-01-02 15:04:05")
	userList         = []User{
		User{1, "root", "070424e5398ec581c27100a0d63fc86e", "", 2},
		User{testID, "cheminlin", "a5b8fedaf75e5396b3ae2c6e60b55da6", "cheminlin@cepave.com", 2},
	}
)

type User struct {
	Id     int
	Name   string
	Passwd string
	email  string
	role   int
}

func main() {

	initDb_uic()
	initDb_falcon_portal()

}

func initDb_falcon_portal() {
	dbName := dbAddr + "falcon_portal" + dbConfig

	db, err := sql.Open("mysql", dbName)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	initTb_action(db)
	initTb_host(db)
	initTb_tpl(db)
	initTb_strategy(db)
	initTb_grp(db)
	initTb_grp_host(db)
	initTb_grp_tpl(db)
}

func initTb_action(db *sql.DB) {
	_, err := db.Exec(
		`
		INSERT INTO action (id, uic, url, callback, before_callback_sms, before_callback_mail, after_callback_sms, after_callback_mail) 
		VALUES (?, 'test_user_group', '', 0, 0, 0, 0, 0)
		`, testID+int('a'))

	if err != nil {
		log.Println(err)
	}
}

func initTb_host(db *sql.DB) {
	_, err := db.Exec(
		`
		INSERT INTO host (id, hostname, ip, agent_version, plugin_version, maintain_begin, maintain_end, update_at)
		VALUES (?, ?, '10.20.30.40', '0.0.1', 'plugin not enabled', 0, 0, ?)
		`, testID+int('h'), testAgent, timeStamp)

	if err != nil {
		log.Println(err)
	}
}

func initTb_grp(db *sql.DB) {
	_, err := db.Exec(
		`
		INSERT INTO grp (id, grp_name, create_user, create_at, come_from)
		VALUES (?, 'test_host_group', 'root', ?, 1)
		`, testID+int('g'), timeStamp)

	if err != nil {
		log.Println(err)
	}
}

func initTb_grp_host(db *sql.DB) {
	_, err := db.Exec(
		`
		INSERT INTO grp_host (grp_id, host_id)
		VALUES (?, ?)
		`, testID+int('g'), testID+int('h'))

	if err != nil {
		log.Println(err)
	}
}

func getHostID(db *sql.DB, hostname string) int {
	var id int
	err := db.QueryRow("SELECT id FROM host WHERE hostname=?", hostname).Scan(&id)
	if err != nil {
		log.Println(err)
	}
	return id
}

func initTb_grp_tpl(db *sql.DB) {
	_, err := db.Exec(
		`
		INSERT INTO grp_tpl (grp_id, tpl_id, bind_user)
		VALUES (?, ?, 'root')
		`, testID+int('g'), testID+int('t'))

	if err != nil {
		log.Println(err)
	}
}

func initTb_tpl(db *sql.DB) {
	_, err := db.Exec(
		`
		INSERT INTO tpl (id, tpl_name, parent_id, action_id, create_user, create_at)
		VALUES (?, 'test_template', 0, ?, 'root', ?)
		`, testID+int('t'), testID+int('a'), timeStamp)

	if err != nil {
		log.Println(err)
	}
}

func initTb_strategy(db *sql.DB) {
	_, err := db.Exec(
		`
		INSERT INTO strategy (id, metric, tags, max_step, priority, func, op, right_value, note, run_begin, run_end, tpl_id)
		VALUES (?, 'cpu.idle', '', 3, 0, 'all(#2)', '<=', 100, '', '', '', ?)
		`, testID+int('s'), testID+int('t'))

	if err != nil {
		log.Println(err)
	}
}

func initDb_uic() {
	dbName := dbAddr + "uic" + dbConfig

	db, err := sql.Open("mysql", dbName)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	initTb_user(db)
	initTb_team(db)
	initTb_rel_team_user(db)
}

func initTb_rel_team_user(db *sql.DB) {
	for k, v := range userList {
		_, err := db.Exec(
			`
			INSERT INTO rel_team_user (id, tid, uid)
			VALUES (?, ?, ?)
			`, testID+k, testID, v.Id)

		if err != nil {
			log.Println(err)
		}
	}
}

func initTb_team(db *sql.DB) {
	_, err := db.Exec(
		`
		INSERT INTO team(id, name, resume, creator, created)
		VALUES (?, "test_user_group", "", 1, ?)
		`, testID, timeStamp)

	if err != nil {
		log.Println(err)
	}
}

func initTb_user(db *sql.DB) {
	for _, v := range userList {
		if exist := check_user_exist(db, v.Name); exist == false {
			log.Println("Insert User:", v.Name)
			_, err := db.Exec(
				`
				INSERT INTO user(id, name ,passwd, email, role, creator, created) 
				VALUES (?, ?, ?, ?, ?, 0, ?)
				`, v.Id, v.Name, v.Passwd, v.email, v.role, timeStamp)

			if err != nil {
				log.Println("[ERROR] Insert user:", v.Name)
				log.Println(err)
			}
		}
	}
}

func check_user_exist(db *sql.DB, username string) bool {
	var id int
	err := db.QueryRow("SELECT id FROM user WHERE name=?", username).Scan(&id)
	switch {
	case err == sql.ErrNoRows:
		log.Println("No user with name:", username)
		return false
	case err != nil:
		log.Fatal(err)
	default:
		fmt.Printf("(Name, ID) = (%s, %v)\n", username, id)
	}
	return true
}
