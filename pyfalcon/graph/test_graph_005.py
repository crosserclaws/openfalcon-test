#!/usr/bin/env python3
""" Functional test of HTTP: graph/index/updateAll. """

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
            "data": "ok"
        }
    }
])
def test_indexUpdateAll(gCfg, graphCfg, host, logger, tCase):
    """
    Functional test of HTTP: graph/index/updateAll.
    The function sends a GET request; then tests resp `dict`.
    
    :param dict gCfg: Global config in json.
    :param dict graphCfg: Graph config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    kwargs = graphCfg['httpApi']['indexUpdateAll']
    httpClient = PyHttp(host, graphCfg['http'], logger)
    r = httpClient.call(**kwargs)
    
    expt = tCase['expect']
    real = r.json()
    assert expt == real