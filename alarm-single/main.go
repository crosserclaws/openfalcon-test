package main

import (
	"fmt"
	"time"

	ag "github.com/open-falcon/agent/g"
	"github.com/open-falcon/common/model"
	jg "github.com/open-falcon/judge/g"
)

var (
	agentConfig string = "agent.json"
	judgeConfig string = "judge.json"
)

func main() {

	test_rpc_hbs()
	test_rpc_transfer()

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

func test_rpc_transfer() {
	ag.ParseConfig(agentConfig)
	ag.InitRpcClients()
	debug := ag.Config().Debug

	// Periodically send metrics
	for {
		now := time.Now().Unix()
		value := now % 100
		metrics := []*model.MetricValue{}
		mv := &model.MetricValue{"test-agent", "cpu.idle", value, 60, "GAUGE", "module=transfer-test", now}
		metrics = append(metrics, mv)

		if debug {
			fmt.Printf("=> <Total=%d> %v\n", len(metrics), metrics[0])
		}

		var resp model.TransferResponse
		err := ag.TransferClient.Call("Transfer.Update", metrics, &resp)
		if err != nil {
			fmt.Println("[ERROR] Transfer.Update:", err)
		}

		if debug {
			fmt.Println("<=", &resp)
		}

		time.Sleep(time.Minute)
	}
}
