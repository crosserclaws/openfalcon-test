#!/usr/bin/env python3

import os
import json
import logging
import argparse
import requests

logFormat = '[%(name)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'
logLevel = logging.DEBUG
CFG_NAME = 'config.json'

def init(loggerName, cfgFileName, suiteFileName, parserCallback=None):
    # Args
    parser = argparse.ArgumentParser()
    _setParser(parser)
    if parserCallback:
        parserCallback(parser)
    args = parser.parse_args()
    # Logger
    logger = newLogger(loggerName)
    logger.setLevel(args.loglevel)
    # Files
    cfg = loadJson(logger, cfgFileName)
    suite = loadJson(logger, suiteFileName)
    
    return logger, cfg, suite, args

def runTestSuite(suiteName, callback, logger, suite, *args):
    passCount = 0
    failCount = 0
    allPass = True
    for idx, tCase in enumerate(suite):
        onePass = None
        logger.info("[%s][#%02d] testing...", suiteName ,idx)
        if logger.getEffectiveLevel() <= logging.INFO:
            onePass = callback(logger, tCase, *args)
        else:
            try:
                onePass = callback(logger, tCase, *args)
            except Exception as e:
                onePass = False
                logger.debug(e)
        
        oneMsg = "[{:s}][#{:02d}] ".format(suiteName, idx)
        # Case report
        if onePass:
            passCount += 1
            oneMsg += "PASS"
        else:
            failCount += 1
            oneMsg += "FAIL"
        print(oneMsg)
    
    # Suite report
    allMsg = "[{:s}][ALL] Total: {:d} Pass: {:d} Fail: {:d}".format(suiteName, passCount+failCount, passCount, failCount)
    print(allMsg)

def newLogger(loggerName=None):
    logger = logging.getLogger(loggerName)
    handler = logging.StreamHandler()
    handler.setLevel(logLevel)
    formatter = logging.Formatter(logFormat)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def loadJson(logger, fileName):
    logger.info("[FILE.] %s", fileName)
    with open(fileName) as data_file:
        json_obj = json.load(data_file)
        logger.debug("[JSON.] %s", json_obj)
        return json_obj

def login(logger, url, param):
    r = requests.post(url, data=param)
    checkBadCode(logger, r)

    sig = r.cookies['sig']
    logger.debug("[SIG.] %s", sig)
    return sig

def checkBadCode(logger, resp):
    if resp.status_code == 200:
        logger.info("[HTTP.] %d", resp.status_code)
        logger.debug("[HTTP.] %s", resp.text)
        return
    raise Exception("[HTTP.] %s %s" % (resp.status_code, resp.text))

def getFnameWoExt(magicFile):
    """ Return the file name without extension with given __file__. """
    baseName = os.path.basename(magicFile)
    return os.path.splitext(baseName)[0]

def getAbsFilePath(magicFile):
    """ Return the absolute path of file with given __file__. """
    return os.path.dirname(os.path.abspath(magicFile)) + '/'

def _setParser(parser):
    parser.add_argument(
        '-d', '--debug',
        help="Print debugging msgs.",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose.",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
