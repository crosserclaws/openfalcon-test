#!/usr/bin/env python3
""" Functional test of RPC: Transfer.Update. """

import pytest

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
        },
        "assert": "Update with valid data but get incorrect resp."
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
        },
        "assert": "Update with valid data but get incorrect resp."
    }
])
def test_update(transferCfg, transferRpc, loggerName, tCase):
    """
    Functional test of RPC: Transfer.Update.
    Send a RPC request and test if the resp is valid.
    
    :param dict transferCfg: Transfer config.
    :param PyRpc transferRpc: A RPC client of transfer.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.

    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Update with valid data contains 1 metric to test if it is working normally.
    01           Update with valid data contains 2 metrics to test if it is working normally.
    ==========   ==============================================================
    """
    
    api = transferCfg['rpcApi']['update']
    
    r = transferRpc.call(api, tCase['data'], loggerName=loggerName)
    expt = tCase['expect']
    real = r['result']
    assert expt.items() <= real.items(), tCase['assert']