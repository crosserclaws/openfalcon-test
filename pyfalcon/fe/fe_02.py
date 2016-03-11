#!/usr/bin/env python3

import os
import requests
from fe_00 import authLogin
from fe_01 import userCreate
from pyutil import common

_SUITE_NAME = os.path.splitext(__file__)[0]
_SUITE_DESC = 'API: userQuery.'

def userQuery(logger, url, payload, cookies):
    try:
        r = requests.get(url, params=payload)
        common.checkBadCode(logger, r)
    except Exception as e:
        logger.debug(e)
        r = None
    return r

def test_userQuery(logger, tCase, cfg):
    # Precondition
    testCookies = authLogin(logger, cfg['login']['url'], cfg['login']['auth'])
    if testCookies is None:
        return False
    baseUrl = "http://{:s}:{:d}".format(cfg['host'], cfg['http'])
    createUrl = baseUrl + cfg['api']['userCreate']
    createPay = tCase['data']['userCreate']
    r = userCreate(logger, createUrl, createPay, testCookies)
    if r is None:
        return False
    
    # Arrange
    testUrl = baseUrl + cfg['api']['userQuery']
    testPay = tCase['data']['userQuery']
    expect = tCase['expect']
    
    # Act
    r = userQuery(logger, testUrl, testPay, testCookies)
    if r is None:
        return False
    
    # Assert
    real = r.json()['users'][0]['name']
    if expect == real:
        return True
    
    return False

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, test_userQuery, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
