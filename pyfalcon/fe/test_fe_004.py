#!/usr/bin/env python3

import pytest
from pyutil import pytool
from pyutil.pyhttp import PyHttp

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
        "expect": ""
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
        "expect": ""
    }
])
def test_teamCreate(gCfg, feCfg, host, logger, tCase):
    gHost = gCfg.get('host', None)
    
    acArgs = feCfg['httpApi']['userCreate']
    aqArgs = feCfg['httpApi']['userQuery']
    kwargs = feCfg['httpApi']['teamCreate']
    httpC = PyHttp(host, feCfg['http'], logger)
    
    httpC.keepLoginInfo(gCfg['login'])
    # Precondition
    for data in tCase['assume']['userCreate']:
        _ = httpC.call(**acArgs, payload=data)
    ids = ""
    for data in tCase['assume']['userQuery']:    
        r = httpC.call(**aqArgs, payload=data)
        ids += str(r.json()['users'][0]['id']) + ','
    
    # Act
    tCase['data']['users'] = ids
    r = httpC.call(**kwargs, payload=tCase['data'])
    expt = tCase['expect']
    real = r.json()['msg']
    # Assert
    try:
        assert expt == real
    except AssertionError as e:
        if expt == '' and real == 'name is already existent':
            pass
        else:
            raise