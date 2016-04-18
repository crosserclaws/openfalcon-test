#!/usr/bin/env python3
""" Functional test of HTTP: graph/index/updateAll/concurrent. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
        },
        "expect": {
            "msg": "success",
            "data": 1
        },
        "assert": "A valid call but receive invalid resp, API may have some problems."
    }
])
def test_indexUpdateAllConcurrent(graphCfg, graphHttp, loggerName, tCase):
    """
    Functional test of HTTP: graph/index/updateAll/concurrent.
    Send a GET request; then test if the resp is valid.
    
    :param dict graphCfg: Graph config.
    :param PyHttp graphHttp: A HTTP client of graph.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Send a valid call to test if it is working normally. 
    ==========   ==============================================================
    """
    
    kwargs = graphCfg['httpApi']['indexUpdateAllConcurrent']
    r = graphHttp.call(**kwargs, loggerName=loggerName)
    
    expt = tCase['expect']
    real = r.json()
    assert expt['msg'] == real['msg'], tCase['assert']
    assert isinstance(real['data'], int), tCase['assert']