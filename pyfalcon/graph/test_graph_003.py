#!/usr/bin/env python3
""" Functional test of HTTP: graph/count. """

import pytest
from pyutil import pytool
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
        },
        "expect": {
        }
    }
])
def test_getCount(gCfg, graphCfg, host, logger, tCase):
    """
    Functional test of HTTP: graph/count.
    The function sends a GET request; then checks if resp is an *integer*.
    
    :param dict gCfg: Global config in json.
    :param dict graphCfg: Graph config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    kwargs = graphCfg['httpApi']['getCount']
    httpClient = PyHttp(host, graphCfg['http'], logger)
    r = httpClient.call(**kwargs)
    
    expt = tCase['expect']
    real = r.json()
    assert isinstance(real, int)