#!/usr/bin/env python3

import requests
import http.client
import urllib.parse
from pyutil import common

_suiteName = 'smtp_00'
_suiteDesc = 'SMTP API: /mail.'

def testApiSmtpMail(logger, tCase, cfg):
    # Arrange & Act
    param = tCase['data']
    url = "http://{:s}:{:d}{:s}".format(cfg['host'], cfg['http'], cfg['api'])
    r = requests.post(url, data=param)
    
    # Assert
    real = r.text
    expect = tCase['expect']
    logger.debug("[DATA.] %s ?= %s", expect, real)
    if real == expect:
        return True
    else:
        return False

def main():
    logger, cfg, suite, _ = common.init(_suiteName, common.gCfgName, _suiteName + '.json')
    common.runTestSuite(_suiteName, testApiSmtpMail, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
