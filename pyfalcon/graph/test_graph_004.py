#!/usr/bin/env python3
""" Functional test of HTTP: graph/counter/all. """

import pytest
from pyutil import pytool
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
        },
        "expect": {
            "msg": "success",
            "data": ["Name", "Cnt", "Time", "Other"]
        }
    }
])
def test_getCounterAll(gCfg, graphCfg, host, logger, tCase):
    """
    Functional test of HTTP: graph/counter/all.
    The function sends a GET request; then checks success message and tests keys of every counter in resp.
    
    :param dict gCfg: Global config in json.
    :param dict graphCfg: Graph config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    kwargs = graphCfg['httpApi']['getCounterAll']
    httpClient = PyHttp(host, graphCfg['http'], logger)
    r = httpClient.call(**kwargs)
    
    expt = tCase['expect']
    real = r.json()
    assert expt['msg'] == real['msg']
    counters = real['data']
    exptSet = set(expt['data'])
    for cDict in counters:
        assert exptSet <= set(cDict)