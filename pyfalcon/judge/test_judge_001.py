#!/usr/bin/env python3
""" Functional test of RPC: Judge.Send. """

import pytest

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
        "expect": "",
        "assert": "A valid call but receive incorrect resp, API may have some problems."
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
        "expect": "",
        "assert": "A valid call but receive incorrect resp, API may have some problems."
    }
])
def test_send(judgeCfg, judgeRpc, loggerName, tCase):
    """
    Functional test of RPC: Judge.Send.
    Send a RPC request and test if it is working normally..
    
    :param dict judgeCfg: Judge config.
    :param PyHttp judgeRpc: A HTTP client of judge.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Send valid data contains 1 metric to test if it is working normally.
    01           Send valid data contains 2 metrics to test if it is working normally.
    ==========   ==============================================================
    """
    
    api = judgeCfg['rpcApi']['send']
    
    r = judgeRpc.call(api, tCase['data'], loggerName=loggerName)
    expt = tCase['expect']
    assert expt == r, tCase['assert']