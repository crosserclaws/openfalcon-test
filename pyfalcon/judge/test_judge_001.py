#!/usr/bin/env python3

import pytest
from pyutil.pyrpc import PyRpc

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": [
            {
                "endpoint": "fake.judge.00",
                "metric": "fake.metric.00",
                "value": 0,
                "judgeType": "GAUGE",
                "tags": "tag=t00",
                "timestamp": 1234567890
            }
        ],
        "expect": ""
    },
    {
        "number": "01",
        "data": [
            {
                "endpoint": "fake.judge.0",
                "metric": "fake.metric.0",
                "value": 0,
                "judgeType": "GAUGE",
                "tags": "tag=t0",
                "timestamp": 1234567890
            },
            {
                "endpoint": "fake.judge.1",
                "metric": "fake.metric.1",
                "value": 1,
                "judgeType": "COUNTER",
                "tags": "tag=t1",
                "timestamp": 1234567891
            }
        ],
        "expect": ""
    }
])
def test_send(gCfg, judgeCfg, host, logger, tCase):
    api = judgeCfg['rpcApi']['send']
    rpcClient = PyRpc(host, judgeCfg['rpc'], logger)
    
    r = rpcClient.call(api, tCase['data'])
    expt = tCase['expect']
    assert expt == r