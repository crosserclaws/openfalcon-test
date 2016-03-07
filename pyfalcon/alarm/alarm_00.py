#!/usr/bin/env python3

import sys
import json
import argparse
import requests
from pyutil import common

_suiteName = 'alarm_00'
_suiteDesc = 'The API of ALARM/event.'

def init(loggerName, cfgFileName, suiteFileName):
    # Args
    parser = argparse.ArgumentParser()
    common.setParser(parser)
    args = parser.parse_args()
    # Logger
    logger = common.newLogger(loggerName)
    logger.setLevel(args.loglevel)
    # Files
    cfg = common.loadJson(logger, cfgFileName)
    suite = common.loadJson(logger, suiteFileName)
    
    return logger, cfg, suite

def testGetEvent(logger, cfg, param, expect):
    # Arrange
    loginUrl = cfg['login']['url']
    loginParam = cfg['login']['auth']
    r = requests.post(loginUrl, data=loginParam)
    sig = r.cookies['sig']
    logger.debug("[SIG.] %s", sig)
    
    # Act
    testUrl = cfg['host'] + ':' + str(cfg['port']) + cfg['api']
    testCookie = dict(sig=sig)
    r = requests.get(testUrl, cookies=testCookie)
    
    # Assert
    expectData = expect['counter']
    eventList = r.json()
    for event in eventList:
        realData = event['counter']
        logger.debug("[DATA.] %s ?= %s", realData, expectData)
        if realData == expectData:
            return True
    logger.debug("[DATA.] All data != %s", expectData)
    return False

def main():
    logger, cfg, suite = init(_suiteName, common.gCfgName, _suiteName + '.json')
    allPass = True

    # Test
    for idx, tCase in enumerate(suite):
        logger.info("[%s][#%02d] testing...", _suiteName ,idx)
        onePass = testGetEvent(logger, cfg, tCase['data'], tCase['expect'])
        oneMsg = "[{:s}][#{:02d}] ".format(_suiteName, idx)
        # Case report
        if onePass:
            oneMsg += "PASS."
        else:
            allPass = False
            oneMsg += "FAIL!"
        print(oneMsg)
            

    # Suite report
    allMsg = "[{:s}][ALL] ".format(_suiteName)
    if allPass:
        allMsg += "PASS."
    else:
        allMsg += "FAIL!"
    print(allMsg)
    

if __name__ == "__main__":
    sys.exit(int(main() or 0))
