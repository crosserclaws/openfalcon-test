#!/usr/bin/env python3

import requests
from pyutil import common

_SUITE_NAME = 'fe_00'
_SUITE_DESC = 'API: authLogin.'

def authLogin(logger, url, payload):
    try:
        r = requests.post(url, data=payload)
        common.checkBadCode(logger, r)
        sig = r.cookies['sig']
        logger.debug("[SIG.] %s", sig)
    except Exception as e:
        logger.debug(e)
        sig = None
    
    return sig

def test_authLogin(logger, tCase, cfg):
    # Arrange
    testUrl = "http://{:s}:{:d}{:s}".format(cfg['host'], cfg['http'], cfg['api']['authLogin'])
    testPayload = tCase['data']
    expect = tCase['expect']
    
    # Act
    sig = authLogin(logger, testUrl, testPayload)
    
    # Assert
    if sig and expect: return True
    if sig is expect: return True
    
    return False

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, test_authLogin, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
