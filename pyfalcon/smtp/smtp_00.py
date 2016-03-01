#!/usr/bin/env python3

import http.client
import urllib.parse
import smtp_util as sutil

__suiteName = 'smtp_00'

def testSendMail(logger, cfg, param, expect):
    # Arrange
    body = urllib.parse.urlencode(param).encode('utf-8')
    headers = { "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain" }
    logger.debug("[REQ->][BODY] %s", body)
    
    # Act
    conn = http.client.HTTPConnection(cfg['host'], cfg['port'])
    conn.request("POST", cfg['url'], body, headers)
    response = conn.getresponse()
    
    logger.debug("[RESP.] %s %s", response.status, response.reason)
    data = response.read()
    conn.close()
    
    # Assert
    expectData = str.encode(expect)
    if data == expectData:
        logger.debug("[DATA.] %s == %s", data, expectData)
        return True
    else:
        logger.debug("[DATA.] %s != %s", data, expectData)
        return False

#
# Program
#

cfg, suite = sutil.init(__suiteName, sutil.gCfgName, __suiteName + '.json')
logger = sutil.getLogger()
allPass = True

# Test
for idx, tCase in enumerate(suite):
    logger.info("Case #%02d testing...", idx)
    onePass = testSendMail(logger, cfg, tCase['data'], tCase['expect'])
    if onePass:
        logger.info("Case #%02d PASS.", idx)
    else:
        allPass = False
        logger.info("Case #%02d FAIL.", idx)

# Report
if allPass:
    print("PASS.")
else:
    print("FAIL.")
