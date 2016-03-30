#!/usr/bin/env python3

import pytest
from pyutil.pyrpc import PyRpc

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": [
            {
                "endpoint": "fake.transfer.00",
                "metric": "fake.metric.00",
                "value": 0,
                "step": 60,
                "counterType": "GAUGE",
                "tags": "tag=t00",
                "timestamp": 1234567890
            }
        ],
        "expect": {
            "Invalid": 0,
            "Total": 1,
            "Message": "ok"
        }
    },
    {
        "number": "01",
        "data": [
            {
                "endpoint": "fake.transfer.0",
                "metric": "fake.metric.0",
                "value": 0,
                "step": 60,
                "counterType": "GAUGE",
                "tags": "tag=t0",
                "timestamp": 1234567890
            },
            {
                "endpoint": "fake.transfer.1",
                "metric": "fake.metric.1",
                "value": 1,
                "step": 60,
                "counterType": "COUNTER",
                "tags": "tag=t1",
                "timestamp": 1234567891
            }
        ],
        "expect": {
            "Invalid": 0,
            "Total": 2,
            "Message": "ok"
        }
    }
])
def test_update(gCfg, transferCfg, host, logger, tCase):
    api = transferCfg['rpcApi']['update']
    rpcClient = PyRpc(host, transferCfg['rpc'], logger)
    
    r = rpcClient.call(api, tCase['data'])
    expt = tCase['expect']
    real = r['result']
    assert expt.items() <= real.items()