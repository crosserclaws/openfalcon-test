#!/usr/bin/env python3

import requests
from fe_00 import authLogin
from pyutil import common

_SUITE_NAME = 'fe_01'
_SUITE_DESC = 'API: userCreate.'

def userCreate(logger, url, payload, cookies):
    try:
        r = requests.post(url, data=payload, cookies={'sig': cookies})
        common.checkBadCode(logger, r)
    except Exception as e:
        logger.debug(e)
        r = None
        
    return r

def test_userCreate(logger, tCase, cfg):
    # Precondition
    testCookies = authLogin(logger, cfg['login']['url'], cfg['login']['auth'])
    if testCookies is None:
        return False
    
    # Arrange
    testUrl = "http://{:s}:{:d}{:s}".format(cfg['host'], cfg['http'], cfg['api']['userCreate'])
    testPayload = tCase['data']
    expect = tCase['expect']
    
    # Act
    r = userCreate(logger, testUrl, testPayload, testCookies)
    if r is None:
        return False
    
    # Assert
    sig = authLogin(logger, cfg['login']['url'], expect)
    if sig is None:
        return False
    
    return True

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, test_userCreate, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
