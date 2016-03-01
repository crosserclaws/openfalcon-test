#!/usr/bin/env python3

import json
import logging
import argparse

_parser = None
_logger = None
logFormat = '[%(name)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s' 
logLevel = logging.DEBUG
gCfgName = 'config.json'

def init(loggerName, cfgFileName, suiteFileName):
    _ = getLogger(loggerName)
    parseArgs()
    cfg = loadJsonFile(cfgFileName)
    suite = loadJsonFile(suiteFileName)
    return cfg, suite
    
def getLogger(loggerName=None):
    global _logger
    if _logger == None:
        _logger = logging.getLogger(loggerName)
        handler = logging.StreamHandler()
        handler.setLevel(logLevel)
        formatter = logging.Formatter(logFormat)
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
    return _logger
    
def getParser():
    global _parser
    if _parser == None:
        _parser = argparse.ArgumentParser()
    return _parser

def parseArgs():
    parser = getParser()
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
    
    args = parser.parse_args()
    global _logger
    _logger.setLevel(args.loglevel)
    
def loadJsonFile(fileName):
    global _logger
    _logger.info("[FILE.] %s", fileName)
    with open(fileName) as data_file:
        json_obj = json.load(data_file)
        _logger.debug("[JSON.] %s", json_obj)
        return json_obj
