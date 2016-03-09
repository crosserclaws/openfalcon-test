#!/usr/bin/env python3

import requests
import http.client
import urllib.parse
from pyutil import common

_SUITE_NAME = 'smtp_00'
_SUITE_DESC = 'API: SMTP/mail.'

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
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, testApiSmtpMail, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
