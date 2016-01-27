package main

import (
	"flag"
	"fmt"
	"time"

	ag "github.com/open-falcon/agent/g"
	"github.com/open-falcon/common/model"
	jg "github.com/open-falcon/judge/g"
)

var (
	agentConfig string = "agent.json"
	judgeConfig string = "judge.json"
	fnList      []func()
)

func main() {
	// Parse cmd-line flags
	var loop, step int
	var mode string
	flag.IntVar(&loop, "loop", 1, "Loop times.")
	flag.IntVar(&step, "step", 60, "Time interval in sec.")
	flag.StringVar(&mode, "mode", "all", "[all, hbs, transfer].")
	flag.Parse()

	switch mode {
	case "hbs":
		fnList = append(fnList, rpcHbsGetStrategies)
	case "transfer":
		fnList = append(fnList, rpcTransferUpdate)
	case "all":
		fnList = append(fnList, rpcHbsGetStrategies)
		fnList = append(fnList, rpcTransferUpdate)
	default:
		flag.Usage()
	}
	// :~)

	// Run periodically
	for i := 1; i <= loop; i++ {
		fmt.Printf("[LOOP.] # %3d\n", i)
		for _, fn := range fnList {
			fn()
		}
		if i < loop {
			time.Sleep(time.Duration(step) * time.Second)
			fmt.Println("")
		}
	}
}

func rpcHbsGetStrategies() {
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

func rpcTransferUpdate() {
	ag.ParseConfig(agentConfig)
	ag.InitRpcClients()

	now := time.Now().Unix()
	value := now % 100
	metrics := []*model.MetricValue{}
	mv := &model.MetricValue{"test-agent", "cpu.idle", value, 60, "GAUGE", "module=transfer-test", now}
	metrics = append(metrics, mv)

	fmt.Printf("[REQ .] <Total=%d> %v\n", len(metrics), metrics[0])

	var resp model.TransferResponse
	err := ag.TransferClient.Call("Transfer.Update", metrics, &resp)
	if err != nil {
		fmt.Println("[ERROR] Transfer.Update:", err)
	}

	fmt.Println("[RESP.]", &resp)
}
