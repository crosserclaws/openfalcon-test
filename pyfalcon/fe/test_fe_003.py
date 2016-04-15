#!/usr/bin/env python3
""" Functional test of HTTP: fe/user/query. """

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
        "expect": "userQuery00",
        "assert": "Give valid data to query user but getting unexpected msg."
    }
])
def test_userQuery(feCfg, feHttp, loggerName, tCase):
    """
    Functional test of HTTP: fe/user/query.
    Send a GET request and test the resp string.
    
    :param dict feCfg: Fe config.
    :param PyHttp feHttp: A HTTP client of fe.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    **Precondition:**
        * API ``userCreate`` may be needed.
        * An account used for login have the authority to create user.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Query a user with valid data to test if it is working normally.
    ==========   ==============================================================
    """
    
    aArgs = feCfg['httpApi']['userCreate']
    kwargs = feCfg['httpApi']['userQuery']
    
    _ = feHttp.call(payload=tCase['assume']['userCreate'], **aArgs, loggerName=loggerName)
    r = feHttp.call(payload=tCase['data'], **kwargs, loggerName=loggerName)
    
    real = None
    expt = tCase['expect']
    users = r.json()['users']
    for u in users:
        real = u['name']
        if expt == real:
            return
    # Raise AssertionError 
    assert expt == real, tCase['assert']