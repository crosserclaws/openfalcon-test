#!/usr/bin/env python3

import requests
import traceback
from fe_00 import authLogin
from fe_01 import userCreate
from fe_02 import userQuery
from pyutil import common

_SUITE_NAME = 'fe_03'
_SUITE_DESC = 'API: teamCreate.'

def teamCreate(logger, url, payload, cookies):
    try:
        r = requests.post(url, data=payload, cookies={'sig': cookies})
        common.checkBadCode(logger, r)
    except Exception as e:
        logger.debug(e)
        r = None
        
    return r

def test_teamCreate(logger, tCase, cfg):
    # Precondition
    testCookies = authLogin(logger, cfg['login']['url'], cfg['login']['auth'])
    if testCookies is None:
        return False
    baseUrl = "http://{:s}:{:d}".format(cfg['host'], cfg['http'])
    createUrl = baseUrl + cfg['api']['userCreate']
    createPayList = tCase['data']['userCreate']
    for payload in createPayList:
        r = userCreate(logger, createUrl, payload, testCookies)
        if r is None:
            return False
    
    ids = ""
    queryUrl = baseUrl + cfg['api']['userQuery']
    queryPayList = tCase['data']['userQuery']
    for payload in queryPayList:
        r = userQuery(logger, queryUrl, payload, testCookies)
        if r is None:
            return False
        ids += str(r.json()['users'][0]['id']) + ','
    
    # Arrange
    testUrl = "http://{:s}:{:d}{:s}".format(cfg['host'], cfg['http'], cfg['api']['teamCreate'])
    testPayload = tCase['data']['teamCreate']
    testPayload['users'] = ids
    expect = tCase['expect']
    
    # Act
    r = teamCreate(logger, testUrl, testPayload, testCookies)
    if r is None:
        return False
    
    # Assert
    
    
    return True

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, test_teamCreate, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
