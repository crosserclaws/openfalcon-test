#!/usr/bin/env python3

import json
import logging
import argparse

logFormat = '[%(name)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'
logLevel = logging.DEBUG
gCfgName = 'config.json'

def newLogger(loggerName=None):
    logger = logging.getLogger(loggerName)
    handler = logging.StreamHandler()
    handler.setLevel(logLevel)
    formatter = logging.Formatter(logFormat)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def setParser(parser):
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

def loadJson(logger, fileName):
    logger.info("[FILE.] %s", fileName)
    with open(fileName) as data_file:
        json_obj = json.load(data_file)
        logger.debug("[JSON.] %s", json_obj)
        return json_obj
