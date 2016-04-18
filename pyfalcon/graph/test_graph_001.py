#!/usr/bin/env python3
""" Functional test of HTTP: graph/api/recv. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": [
            "test_apiRecv_host", "cpu.user", 1456286162, 60, "GAUGE", 0.3579
        ],
        "expect": {
            "msg": "success",
            "data": "ok"
        },
        "assert": "A valid call but receive unexpected resp, API may have some problems."
    },
    {
        "number": "01",
        "data": [
            "test_apiRecv_host", "cpu.user", 1456286162, 60
        ],
        "expect": {
            "msg": "success",
            "data": "bad args"
        },
        "assert": "Give incorrect number of params but receive unexpected error msg."
    }
])
def test_apiRecv(graphCfg, graphHttp, loggerName, tCase):
    """
    Functional test of HTTP: graph/api/recv.
    Send a GET request; then test if the resp is valid.
    
    :param dict graphCfg: Graph config.
    :param PyHttp graphHttp: A HTTP client of graph.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    .. note:: Make sure that the data should in the same order as
              **endpoint/metric/ts/step/dstype/value** whose types are str/str/int/int/str/float.
              
              Here is an URL example: HOST_ADDR/api/recv/host1/cpu.user/1456286162/60/GAUGE/0.3579.

    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Send a valid call to test if it is working normally.
    01           Send with incorrect number of params to test if it is working normally.
    ==========   ==============================================================
    """
    
    # Special URL case
    kwargs = graphCfg['httpApi']['apiRecv']
    data = tCase['data']
    kwargs['api'] = kwargs['api'] + '/' + '/'.join(map(str, data))
    r = graphHttp.call(**kwargs, loggerName=loggerName)
    
    expt = tCase['expect']
    real = r.json() 
    assert expt == real, tCase['assert']