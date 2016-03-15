#!/usr/bin/env python3

import requests
from pyutil import common

_SUITE_DESC = 'API: ALARM/event.'
_SUITE_NAME = common.getFnameWoExt(__file__)
MODULE_PATH = common.getAbsFilePath(__file__)

def _checkLogin(logger, cfg):
    if cfg['debug']: return None
    
    loginUrl = cfg['login']['url']
    loginParam = cfg['login']['auth']
    r = requests.post(loginUrl, data=loginParam)
    sig = r.cookies['sig']
    logger.debug("[SIG.] %s", sig)
    
    return sig

def testGetEvent(logger, tCase, cfg):
    # Arrange
    sig = _checkLogin(logger, cfg)
    testUrl = "http://{:s}:{:d}{:s}".format(cfg['host'], cfg['http'], cfg['api'])
    testCookie = dict(sig=sig)
    # Act
    r = requests.get(testUrl, cookies=testCookie)
    
    # Assert
    expect = tCase['expect']['counter']
    eventList = r.json()
    logger.debug("[RES<-]\n%s", eventList)
    for event in eventList:
        real = event['counter']
        logger.debug("[DATA.] %s ?= %s", expect, real)
        if expect == real:
            return True
    
    return False

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, MODULE_PATH + common.CFG_NAME, MODULE_PATH + _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, testGetEvent, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
