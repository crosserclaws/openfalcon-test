#!/usr/bin/env python3

import pytest
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
            "name": "root",
            "password": "root"
        },
        "expect": ""
    },
    {
        "number": "01",
        "data": {
            "name": "",
            "password": "arbitrary_pw"
        },
        "expect": "name or password is blank"
    },
    {
        "number": "02",
        "data": {
            "name": "arbitrary_user",
            "password": ""
        },
        "expect": "name or password is blank"
    }
])
def test_authLogin(gCfg, feCfg, host, logger, tCase):
    kwargs = feCfg['httpApi']['authLogin']
    httpC = PyHttp(host, feCfg['http'], logger)
    
    r = httpC.call(payload=tCase['data'], **kwargs)
    expt = tCase['expect']
    real = r.json()['msg']
    assert expt == real