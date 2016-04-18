#!/usr/bin/env python3
""" Functional test of HTTP: graph/count. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
        },
        "expect": 0,
        "assert": "A valid call but receive invalid resp, API may have some problems."
    }
])
def test_getCount(graphCfg, graphHttp, loggerName, tCase):
    """
    Functional test of HTTP: graph/count.
    The function sends a GET request; then checks if resp is an *integer*.
    
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
    
    kwargs = graphCfg['httpApi']['getCount']
    r = graphHttp.call(**kwargs, loggerName=loggerName)
    
    expt = tCase['expect']
    real = r.json()
    exptType = type(expt)
    realType = type(real)
    assert exptType == realType, tCase['assert']