#!/usr/bin/env python3
""" Functional test of HTTP: fe/me/user/c. """

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
    """
    Functional test of HTTP: fe/me/user/c which is login needed.
    The function sends a POST request and check resp string.
    
    :param dict gCfg: Global config in json.
    :param dict feCfg: Fe config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    kwargs = feCfg['httpApi']['userCreate']
    httpClient = PyHttp(host, feCfg['http'], logger)
    
    httpClient.keepLoginInfo(gCfg['login'])
    r = httpClient.call(payload=tCase['data'], **kwargs)
    expt = tCase['expect']
    real = r.json()['msg']
    try:
        assert expt == real
    except AssertionError as e:
        if expt == '' and real == 'name is already existent':
            pass
        else:
            raise