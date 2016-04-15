#!/usr/bin/env python3
""" Functional test of HTTP: fe/auth/login. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
            "name": "root",
            "password": "error_password"
        },
        "expect": "password error",
        "assert": "Login with incorrect pwd but get unexpected error msg."
    },
    {
        "number": "01",
        "data": {
            "name": "",
            "password": "arbitrary_pw"
        },
        "expect": "name or password is blank",
        "assert": "Login with blank username but get unexpected error msg."
    },
    {
        "number": "02",
        "data": {
            "name": "arbitrary_user",
            "password": ""
        },
        "expect": "name or password is blank",
        "assert": "Login with blank pwd but get unexpected error msg."
    }
])
def test_authLogin(feCfg, feHttp, loggerName, tCase):
    """
    Functional test of HTTP: fe/auth/login.
    Send a POST request and test the resp string.
    
    :param dict feCfg: Fe config.
    :param PyHttp feHttp: A HTTP client of fe.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Login with incorrect pwd and get the expected error msg.
    01           Login with blank username and get the expected error msg.
    02           Login with blank pwd and get the expected error msg.
    ==========   ==============================================================
    """
    
    kwargs = feCfg['httpApi']['authLogin']
    
    r = feHttp.call(payload=tCase['data'], **kwargs, loggerName=loggerName)
    expt = tCase['expect']
    real = r.json()['msg']
    assert expt == real, tCase['assert']