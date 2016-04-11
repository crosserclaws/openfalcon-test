#!/usr/bin/env python3
""" Functional test of HTTP: fe/auth/login. """

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
    """
    Functional test of HTTP: fe/auth/login.
    The function sends a POST request and check resp string.
    
    :param dict gCfg: Global config in json.
    :param dict feCfg: Fe config in json.
    :param str host: Host IP to send the request.
    :param logging.Logger logger: A logger named in the module's name.
    :param dict tCase: A test case in json.
    """
    
    kwargs = feCfg['httpApi']['authLogin']
    httpClient = PyHttp(host, feCfg['http'], logger)
    
    r = httpClient.call(payload=tCase['data'], **kwargs)
    expt = tCase['expect']
    real = r.json()['msg']
    assert expt == real