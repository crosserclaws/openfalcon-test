#!/usr/bin/env python3

"""Pyfalcon - A testing framework in pure Python3 for Open-Falcon.

Usage:
  pyfalcon.py [-m <module> [-s <suite>]] [-v | -d]
  pyfalcon.py -h

Options:
  -d --debug                     Show debugging msgs.
  -h --help                      Show this screen.
  -v --verbose                   Show detail msgs.
  -m <module> --module=<module>  Specify a module to test. (Run all tests if not sepecified.)
                                 {'alarm', 'fe', 'hbs', 'judge', 'smtp', 'transfer'}
  -s <suite> --suite=<suite>     Specify a suite number to test.
  
"""

import os
import logging
import subprocess
from docopt import docopt

SUITE_MAX = 100
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_MODULE = ['alarm', 'fe', 'hbs', 'judge', 'smtp', 'transfer']

handleLevel = logging.DEBUG
logFormat = '[%(name)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'


def init(loggerName):
    # Args
    optDic = docopt(__doc__)
    
    # Logger
    logger = newLogger(loggerName)
    if optDic['--verbose']: logger.setLevel(logging.INFO)
    if optDic['--debug']: logger.setLevel(logging.DEBUG)
    
    logger.debug('[DocOpt]\n%s', optDic)
    return logger, optDic

def newLogger(loggerName=None):
    logger = logging.getLogger(loggerName)
    handler = logging.StreamHandler()
    handler.setLevel(handleLevel)
    formatter = logging.Formatter(logFormat)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def testOneModule(logger, optDic, moduleName):
    logger.info('[Module] %s', moduleName)
    suite = optDic['--suite']
    
    if suite:
        suiteName = moduleName + '_' + suite.zfill(2)
        testOneSuite(logger, optDic, suiteName)
    else:
        for idx in range(SUITE_MAX):
            suiteName = moduleName + '_' + str(idx).zfill(2)
            testOneSuite(logger, optDic, suiteName)
    

def testOneSuite(logger, optDic, suiteName):
    logger.info('[Suite] %s', suiteName)

def main():
    baseName = os.path.basename(__file__)
    logger, optDic = init(os.path.splitext(baseName)[0])
    
    # Module mode
    mod = optDic['--module']
    if mod: 
        if mod in TEST_MODULE:
            testOneModule(logger, optDic, mod)
        else:
            logger.info('[Module] Invalid name: %s', mod)
        return
    
    # All mode
    logger.info('[AllMod] %s', TEST_MODULE)
    for mod in TEST_MODULE:
        testOneModule(logger, optDic, mod)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))