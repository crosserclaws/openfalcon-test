#!/usr/bin/env python3

import requests
from pyutil import common

_SUITE_NAME = 'fe_01'
_SUITE_DESC = 'API: FE/me/user/c.'

def testUserCreate(logger, tCase, cfg):
    # Arrange
    loginUrl = cfg['login']['url']
    sig = common.login(logger, loginUrl, cfg['login']['auth'])
    testUrl = "http://{:s}:{:d}{:s}".format(cfg['host'], cfg['http'], cfg['api']['userCreate'])
    testParam = tCase['data']
    
    # Act
    r = requests.post(testUrl, data=testParam, cookies={'sig': sig})
    common.checkBadCode(logger, r)
    
    
    # Assert
    _ = common.login(logger, loginUrl, tCase['expect'])
    return True

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, testUserCreate, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
