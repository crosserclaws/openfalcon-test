#!/usr/bin/env python3
""" Functional test of HTTP: graph/index/updateAll/concurrent. """

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
            "data": 1
        }
    }
])
def test_indexUpdateAllConcurrent(gCfg, graphCfg, host, logger, tCase):
    """
    Functional test of HTTP: graph/index/updateAll/concurrent.
    The function sends a GET request; then tests success message and `int` number of concurrent threads.
    
    :param dict gCfg: Global config in json.
    :param dict graphCfg: Graph config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    kwargs = graphCfg['httpApi']['indexUpdateAllConcurrent']
    httpClient = PyHttp(host, graphCfg['http'], logger)
    r = httpClient.call(**kwargs)
    
    expt = tCase['expect']
    real = r.json()
    assert expt['msg'] == real['msg']
    assert isinstance(real['data'], int)