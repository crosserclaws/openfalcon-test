#!/usr/bin/env python3
""" Functional test of RPC: Judge.Send. """

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
    """
    Functional test of RPC: Judge.Send.
    The function sends a RPC request and check the ``void`` resp.
    
    :param dict gCfg: Global config in json.
    :param dict judgeCfg: Judge config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    api = judgeCfg['rpcApi']['send']
    rpcClient = PyRpc(host, judgeCfg['rpc'], logger)
    
    r = rpcClient.call(api, tCase['data'])
    expt = tCase['expect']
    assert expt == r