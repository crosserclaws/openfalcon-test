#!/usr/bin/env python3

import json
import logging
import argparse

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
    allPass = True
    for idx, tCase in enumerate(suite):
        onePass = None
        logger.info("[%s][#%02d] testing...", suiteName ,idx)
        try:
            onePass = callback(logger, tCase, *args)
        except Exception as e:
            onePass = False
            logger.debug(e)
        
        oneMsg = "[{:s}][#{:02d}] ".format(suiteName, idx)
        # Case report
        if onePass:
            oneMsg += "PASS."
        else:
            allPass = False
            oneMsg += "FAIL!"
        print(oneMsg)
    
    # Suite report
    allMsg = "[{:s}][ALL] ".format(suiteName)
    if allPass:
        allMsg += "PASS."
    else:
        allMsg += "FAIL!"
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
