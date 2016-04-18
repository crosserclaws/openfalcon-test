#!/usr/bin/env python3
""" Functional test of HTTP: graph/index/updateAll. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {},
        "expect": {
            "msg": "success",
            "data": "ok"
        },
        "assert": "A valid call but receive unexpected resp, API may have some problems."
    }
])
def test_indexUpdateAll(graphCfg, graphHttp, loggerName, tCase):
    """
    Functional test of HTTP: graph/index/updateAll.
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
    
    kwargs = graphCfg['httpApi']['indexUpdateAll']
    r = graphHttp.call(**kwargs, loggerName=loggerName)
    
    expt = tCase['expect']
    real = r.json()
    assert expt == real, tCase['assert']