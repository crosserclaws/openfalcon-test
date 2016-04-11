#!/usr/bin/env python3
""" Functional test of HTTP: alarm/event. """

import pytest
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
        },
        "expect":[
        ]
    },
    pytest.mark.xfail({
        "number": "01",
        "data": {
        },
        "expect": [
            {
                "counter": "fake-agent/cpu.idle module=transfer-fake"
            }
        ]
    })
])
def test_getEvent(gCfg, alarmCfg, host, logger, tCase):
    """
    Functional test of HTTP: alarm/event which is login needed.
    The function sends a GET request and check the *list* that ``expt <= resp``.
    
    :param dict gCfg: Global config in json.
    :param dict alarmCfg: Alarm config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    kwargs = alarmCfg['httpApi']['getEvent']
    httpClient = PyHttp(host, alarmCfg['http'], logger)
    
    httpClient.keepLoginInfo(gCfg['login'])
    r = httpClient.call(payload=tCase['data'], **kwargs)
    expt = tCase['expect']
    real = r.json()
    assert expt <= real