#!/usr/bin/env python3
""" Functional test of HTTP: fe/me/team/c. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "assume": {
            "userCreate":[
                {
                    "name": "createTeam-user00",
                    "password": "fakepw",
                    "email": "fakemail@cepave.com"
                }
            ],
            "userQuery": [
                {
                    "query": "createTeam-user00"
                }
            ]
        },
        "data": {
            "name": "createTeam00",
            "resume": "",
            "users": "USER_ID"
        },
        "expect": "",
        "assert": "Create team with valid data but get unexpected msg."
    },
    {
        "number": "01",
        "assume": {
            "userCreate":[
                {
                    "name": "createTeam01-user00",
                    "password": "fakepw",
                    "email": "fakemail@cepave.com"
                },
                {
                    "name": "createTeam01-user01",
                    "password": "fakepw",
                    "email": "fakemail@cepave.com"
                }
            ],
            "userQuery": [
                {
                    "query": "createTeam01-user00"
                },
                {
                    "query": "createTeam01-user01"
                }
            ]
        },
        "data": {
            "name": "createTeam01",
            "resume": "",
            "users": "USER_ID_010, USER_ID_011"
        },
        "expect": "",
        "assert": "Create team with valid data but get unexpected msg."
    }
])
def test_teamCreate(feCfg, feHttp, loggerName, tCase):
    """
    Functional test of HTTP: fe/me/team/c which is login needed.
    Send a POST request and test the resp string.
    
    :param dict feCfg: Fe config.
    :param PyHttp feHttp: A HTTP client of fe.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    **Precondition:**
        * API ``userCreate`` and ``userQuery`` are working normally.
        * An account used for login have the authority to create team and user.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Create a team with a valid user data to test if it is working normally.
    01           Create a team with 2 valid user data to test if it is working normally.
    ==========   ==============================================================
    """
    
    acArgs = feCfg['httpApi']['userCreate']
    aqArgs = feCfg['httpApi']['userQuery']
    kwargs = feCfg['httpApi']['teamCreate']
    
    # Precondition
    for data in tCase['assume']['userCreate']:
        _ = feHttp.call(**acArgs, payload=data, loggerName=loggerName)
    ids = ""
    for data in tCase['assume']['userQuery']:    
        r = feHttp.call(**aqArgs, payload=data, loggerName=loggerName)
        ids += str(r.json()['users'][0]['id']) + ','
    
    # Act
    tCase['data']['users'] = ids
    r = feHttp.call(**kwargs, payload=tCase['data'], loggerName=loggerName)
    expt = tCase['expect']
    real = r.json()['msg']
    # Assert
    try:
        assert expt == real, tCase['assert']
    except AssertionError as e:
        if expt == '' and real == 'name is already existent':
            pass
        else:
            raise