#!/usr/bin/env python3
""" Functional test of HTTP: transfer/api/push. """

import json
import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": [
            {
                "endpoint": "bgp-bj-058-083-161-105",
                "metric": "cpu.idle",
                "value": 0.7857,
                "step": 1,
                "counterType": "COUNTER",
                "tags": "tag",
                "timestamp": 1452493440
            }
        ],
        "expect": {
            "msg": "success",
            "data": {
                "Message": "ok",
                "Total": 1,
                "Invalid": 0,
                "Latency": 0
            }
        },
        "assert": "Push with valid data but get incorrect resp."
    }
])
def test_apiPush(transferCfg, transferHttp, loggerName, tCase):
    """
    Functional test of HTTP: transfer/api/push.
    Send a POST request and test if the resp is valid.
    
    :param dict transferCfg: Transfer config.
    :param PyHttp transferHttp: A HTTP client of transfer.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Push with valid data to test if it is working normally.
    ==========   ==============================================================
    """
    
    kwargs = transferCfg['httpApi']['apiPush']
    
    # Convert list into string for raw payload.
    r = transferHttp.call(payload=json.dumps(tCase['data']), **kwargs, loggerName=loggerName)
    expt = tCase['expect']
    real = r.json()
    assert expt == real, tCase['assert']