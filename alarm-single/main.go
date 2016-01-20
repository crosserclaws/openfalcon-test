package main

import (
	"fmt"

	"github.com/open-falcon/common/model"
	jg "github.com/open-falcon/judge/g"
)

var (
	judgeConfig string = "judge.json"
)

func main() {

	test_rpc_hbs()

}

func test_rpc_hbs() {
	jg.ParseConfig(judgeConfig)
	jg.InitHbsClient()

	var resp model.StrategiesResponse
	err := jg.HbsClient.Call("Hbs.GetStrategies", model.NullRpcRequest{}, &resp)
	if err != nil {
		fmt.Println("[ERROR] Hbs.GetStrategies:", err)
		return
	}

	fmt.Println("[RESP.] Hbs.GetStrategies:", resp)
	for k, v := range resp.HostStrategies {
		fmt.Printf("Idx:%v, Hostname:%v, Strategies:%v\n", k, v.Hostname, v.Strategies)
	}
}
