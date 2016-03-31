#!/usr/bin/env python3

import pytest
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "assume": {
            "userCreate": {
                "name": "userQuery00",
                "password": "fakepw",
                "email": "fakemail@cepave.com"
            }
        },
        "data": {
            "query": "userQuery00"
        },
        "expect": "userQuery00"
    }
])
def test_userQuery(gCfg, feCfg, host, logger, tCase):
    aArgs = feCfg['httpApi']['userCreate']
    kwargs = feCfg['httpApi']['userQuery']
    httpClient = PyHttp(host, feCfg['http'], logger)
    httpClient.keepLoginInfo(gCfg['login'])
    
    _ = httpClient.call(payload=tCase['assume']['userCreate'], **aArgs)
    r = httpClient.call(payload=tCase['data'], **kwargs)
    
    real = None
    expt = tCase['expect']
    users = r.json()['users']
    for u in users:
        real = u['name']
        if expt == real:
            return
    # Raise AssertionError 
    assert expt == real