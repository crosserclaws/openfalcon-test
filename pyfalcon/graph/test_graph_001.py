#!/usr/bin/env python3
""" Functional test of HTTP: graph/api/recv. """

import pytest
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": [
            "test_apiRecv_host", "cpu.user", 1456286162, 60, "GAUGE", 0.3579
        ],
        "expect": {
            "msg": "success",
            "data": "ok"
        }
    },
    {
        "number": "01",
        "data": [
            "test_apiRecv_host", "cpu.user", 1456286162, 60
        ],
        "expect": {
            "msg": "success",
            "data": "bad args"
        }
    }
])
def test_apiRecv(gCfg, graphCfg, host, logger, tCase):
    """
    Functional test of HTTP: graph/api/recv.
    The function sends a GET request; then tests resp `dict`.
    
    :param dict gCfg: Global config in json.
    :param dict graphCfg: Graph config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    
    .. note:: Make sure that the data should in the same order as
              **endpoint/metric/ts/step/dstype/value** whose types are str/str/int/int/str/float.
              
              Here is an URL example: HOST_ADDR/api/recv/host1/cpu.user/1456286162/60/GAUGE/0.3579.
    """
    
    # Special URL case
    kwargs = graphCfg['httpApi']['apiRecv']
    httpClient = PyHttp(host, graphCfg['http'], logger)
    data = tCase['data']
    kwargs['api'] = kwargs['api'] + '/' + '/'.join(map(str, data))
    r = httpClient.call(**kwargs)
    
    expt = tCase['expect']
    real = r.json() 
    assert expt == real