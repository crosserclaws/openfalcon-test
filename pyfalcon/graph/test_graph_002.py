#!/usr/bin/env python3
""" Functional test of HTTP: graph/config. """

import pytest
from pyutil import pytool
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    pytest.mark.skipif(pytest.config.getvalue('--dev'), reason='Inconsistent config file version.') ({
        "number": "00",
        "data": {
        },
        "expect": {
            "msg": "success",
            "data": {
                "pid": "",
                "debug": False,
                "http": {
                    "enabled": True,
                    "listen": "0.0.0.0:6071"
                },
                "rpc": {
                    "enabled": True,
                    "listen": "0.0.0.0:6070"
                },
                "rrd": {
                    "storage": "/home/graph/data/6070"
                },
                "db": {
                    "dsn": "user:password@tcp(250.251.252.253:3306)/graph?loc=Local&parseTime=true",
                    "maxIdle": 4
                }
            }
        }
    }),
    pytest.mark.skipif(not pytest.config.getvalue('--dev'), reason='Inconsistent config file version.') ({
        "number": "01",
        "data": {
        },
        "expect": {
            "msg": "success",
            "data": {
                "pid": "",
                "debug": False,
                "http": {
                    "enable": True,
                    "listen": "0.0.0.0:6071"
                },
                "rpc": {
                    "enable": True,
                    "listen": "0.0.0.0:6070"
                },
                "rrd": {
                    "storage": "/home/graph/data/6070"
                },
                "db": {
                    "dsn": "user:password@tcp(250.251.252.253:3306)/graph?loc=Local&parseTime=true",
                    "maxIdle": 4
                }
            }
        }
    })
])
def test_getConfig(gCfg, graphCfg, host, logger, tCase):
    """
    Functional test of HTTP: graph/config.
    The function sends a GET request; then checks success message and recursively tests subset keys in resp.
    
    :param dict gCfg: Global config in json.
    :param dict graphCfg: Graph config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    kwargs = graphCfg['httpApi']['getConfig']
    httpClient = PyHttp(host, graphCfg['http'], logger)
    r = httpClient.call(**kwargs)
    
    expt = tCase['expect']
    real = r.json()
    assert expt['msg'] == real['msg']
    pytool.assertSubsetKeysInDic(expt, real)