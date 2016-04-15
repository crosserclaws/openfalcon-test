#!/usr/bin/env python3
""" Functional test of HTTP: fe/me/user/c. """

import pytest

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
        "expect": "",
        "assert": "Give valid data to create user but get unexpected msg."
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
        "expect": "name pattern is invalid",
        "assert": "Give invalid username to create user but get unexpected msg."
    }
])
def test_userCreate(feCfg, feHttp, loggerName, tCase):
    """
    Functional test of HTTP: fe/me/user/c which is login needed.
    Send a POST request and test the resp string.
    
    :param dict feCfg: Fe config.
    :param PyHttp feHttp: A HTTP client of fe.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    **Precondition:**
        * An account used for login have the authority to create user.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Create a user with valid data to test if it is working normally.
    01           Create a user with invalid username and get the expected error msg.
    ==========   ==============================================================
    """
    
    kwargs = feCfg['httpApi']['userCreate']
    
    r = feHttp.call(payload=tCase['data'], **kwargs, loggerName=loggerName)
    expt = tCase['expect']
    real = r.json()['msg']
    try:
        assert expt == real, tCase['assert']
    except AssertionError as e:
        if expt == '' and real == 'name is already existent':
            pass
        else:
            raise