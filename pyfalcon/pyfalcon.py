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

import logging
import subprocess
from docopt import docopt
from pyutil import common

SUITE_MAX = 100
ROOT_PATH = common.getAbsFilePath(__file__)
TEST_MODULE = ['fe', 'transfer', 'hbs', 'judge', 'alarm', 'smtp']

_msgFlag = ''
_handleLevel = logging.DEBUG
_logFormat = '[%(name)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'


def init(loggerName):
    # Args
    optDic = docopt(__doc__)
    
    # Logger
    global _msgFlag
    logger = newLogger(loggerName)
    if optDic['--verbose']:
        _msgFlag = '-v'
        logger.setLevel(logging.INFO)
    if optDic['--debug']:
        _msgFlag = '-d'
        logger.setLevel(logging.DEBUG)
    
    logger.debug('[DocOpt]\n%s', optDic)
    return logger, optDic

def newLogger(loggerName=None):
    logger = logging.getLogger(loggerName)
    handler = logging.StreamHandler()
    handler.setLevel(_handleLevel)
    formatter = logging.Formatter(_logFormat)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def testOneModule(logger, optDic, moduleName):
    suite = optDic['--suite']
    # A specified test suite
    if suite:
        suiteName = "{0}/{0}_{1}.py".format(moduleName, suite.zfill(2))
        try:
            testOneSuite(logger, optDic, suiteName)
        except subprocess.CalledProcessError as e:
            logger.debug(e.output, e.returncode)
            logger.error('[Suite] Invalid suite number: %s', suiteName)
    # All suites in the module
    else:
        for idx in range(SUITE_MAX):
            suiteName = "{0}/{0}_{1}.py".format(moduleName, str(idx).zfill(2))
            try:
                testOneSuite(logger, optDic, suiteName)
            except subprocess.CalledProcessError as e:
                logger.info('[Ignore] %s', suiteName)
                logger.debug('[Out]\n%s', e.output)
                break

def testOneSuite(logger, optDic, suiteName):
    cmd = ['python3', suiteName, _msgFlag] if _msgFlag else ['python3', suiteName]
    outByte = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    print(outByte.decode())

def main():
    logger, optDic = init(common.getFnameWoExt(__file__))
    
    # One module mode
    mod = optDic['--module']
    if mod: 
        if mod in TEST_MODULE:
            testOneModule(logger, optDic, mod)
        else:
            logger.error('[Module] Invalid name: %s', mod)
        return
    
    # All module mode
    logger.info('[AllMod] %s', TEST_MODULE)
    for mod in TEST_MODULE:
        testOneModule(logger, optDic, mod)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))