#!/usr/bin/env python3
""" Functional test of HTTP: graph/config. """

import pytest

@pytest.mark.parametrize("tCase", [
    pytest.mark.env("glob") ({
        "number": "00",
        "data": {},
        "expect": {
            "msg": "success",
            "data": {
                "pid": [],
                "debug": [],
                "http": ["enabled", "listen"],
                "rpc": ["enabled", "listen"],
                "rrd": ["storage"],
                "db": ["dsn", "maxIdle"]
            }
        },
        "assert": "A valid call but receive invalid resp, API may have some problems."
    }),
    pytest.mark.env("dev") ({
        "number": "01",
        "data": {},
        "expect": {
            "msg": "success",
            "data": {
                "pid": [],
                "debug": [],
                "http": ["enable", "listen"],
                "rpc": ["enable", "listen"],
                "rrd": ["storage"],
                "db": ["dsn", "maxIdle"]
            }
        },
        "assert": "A valid call but receive invalid resp, API may have some problems."
    })
])
def test_getConfig(graphCfg, graphHttp, loggerName, tCase):
    """
    Functional test of HTTP: graph/config.
    Send a GET request; then test if keys are in the resp.
    
    :param dict graphCfg: Graph config.
    :param PyHttp graphHttp: A HTTP client of graph.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Send a valid call to test if it is working normally. (env=global)
    01           Send a valid call to test if it is working normally. (env=dev)
    ==========   ==============================================================
    """
    
    kwargs = graphCfg['httpApi']['getConfig']
    r = graphHttp.call(**kwargs, loggerName=loggerName)
    
    expt = tCase['expect']
    real = r.json()
    assert expt['msg'] == real['msg'], tCase['assert']
    exptData = expt['data']
    realData = real['data']
    for key, val in exptData.items():
        assert key in realData, tCase['assert']
        if val:
            for v in val:
                assert v in realData[key], tCase['assert']