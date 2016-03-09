#!/usr/bin/env python3

import requests
from pyutil import common

_SUITE_NAME = 'fe_00'
_SUITE_DESC = 'API: FE/root.'

def testRootCreate(logger, tCase, cfg):
    # Arrange
    testUrl = "http://{:s}:{:d}{:s}".format(cfg['host'], cfg['http'], cfg['api']['rootCreate'])
    testParam = tCase['data']
    # Act
    r = requests.get(testUrl, params=testParam)
    common.checkBadCode(logger, r)
    
    # Assert
    _ = common.login(logger, cfg['login']['url'], tCase['expect'])
    return True

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, testRootCreate, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
