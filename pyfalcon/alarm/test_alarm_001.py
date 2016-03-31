#!/usr/bin/env python3

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
    kwargs = alarmCfg['httpApi']['getEvent']
    httpClient = PyHttp(host, alarmCfg['http'], logger)
    
    httpClient.keepLoginInfo(gCfg['login'])
    r = httpClient.call(payload=tCase['data'], **kwargs)
    expt = tCase['expect']
    real = r.json()
    assert expt <= real