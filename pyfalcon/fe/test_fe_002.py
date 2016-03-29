#!/usr/bin/env python3

import pytest
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
            "name": "fake-feuser",
            "password": "fakepw",
            "cnname": "",
            "email": "fakemail@cepave.com",
            "phone": "",
            "im": "",
            "qq": ""
        },
        "expect": ""
    },
    {
        "number": "01",
        "data": {
            "name": "dangerous<&>user",
            "password": "arbitrarypw",
            "cnname": "",
            "email": "fakemail@cepave.com",
            "phone": "",
            "im": "",
            "qq": ""
        },
        "expect": "name pattern is invalid"
    }
])
def test_userCreate(gCfg, feCfg, host, logger, tCase):
    kwargs = feCfg['httpApi']['userCreate']
    httpC = PyHttp(host, feCfg['http'], logger)
    
    httpC.keepLoginInfo(gCfg['login'])
    r = httpC.call(payload=tCase['data'], **kwargs)
    expt = tCase['expect']
    real = r.json()['msg']
    try:
        assert expt == real
    except AssertionError as e:
        if expt == '' and real == 'name is already existent':
            pass
        else:
            raise