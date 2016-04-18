#!/usr/bin/env python3
""" Functional test of HTTP: graph/counter/all. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {},
        "expect": {
            "msg": "success",
            "data": ["Name", "Cnt", "Time", "Other"]
        },
        "assert": "A valid call but receive invalid resp, API may have some problems."
    }
])
def test_getCounterAll(graphCfg, graphHttp, loggerName, tCase):
    """
    Functional test of HTTP: graph/counter/all.
    Send a GET request; then test if counters are the subset of resp.
    
    :param dict graphCfg: Graph config.
    :param PyHttp graphHttp: A HTTP client of graph.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    .. note:: Ignore the "Qps" field in counter since not every counter owns that field.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Send a valid call to test if it is working normally.
    ==========   ==============================================================
    """
    
    kwargs = graphCfg['httpApi']['getCounterAll']
    r = graphHttp.call(**kwargs, loggerName=loggerName)
    
    expt = tCase['expect']
    real = r.json()
    assert expt['msg'] == real['msg'], tCase['assert']
    counters = real['data']
    exptSet = set(expt['data'])
    for cDict in counters:
        assert exptSet <= set(cDict), tCase['assert']