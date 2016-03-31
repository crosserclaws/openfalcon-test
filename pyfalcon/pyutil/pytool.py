#!/usr/bin/env python3

import os
import json
import logging

LOG_FORMAT = '[%(name)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'

def getFnameWoExt(magicFile):
    """ Return the file name without extension with given __file__. """
    baseName = os.path.basename(magicFile)
    return os.path.splitext(baseName)[0]

def getDirName(magicFile):
    """ Return the directory name with give __file__. """
    dirPath = os.path.dirname(os.path.abspath(magicFile))
    parts = dirPath.split(os.path.sep)
    return parts[-1]

def getAbsFileDir(magicFile):
    """ Return the absolute path of file with given __file__. """
    return os.path.dirname(os.path.abspath(magicFile)) + '/'

def getAbsParDir(magicFile):
    """ Return the absolute path of file's parent directory with given __file__. """
    sep = os.path.sep
    parts = getAbsFileDir(__file__).split(sep)
    return sep.join(parts[:-2]) + '/'

PYFALCON_DIR = getAbsParDir(__file__)
CONFIG_DIR = PYFALCON_DIR + 'config/'
GLOBAL_CFG_PATH = CONFIG_DIR + 'global.json'

def newLogger(loggerName=None):
    logging.basicConfig(format=LOG_FORMAT)
    logger = logging.getLogger(loggerName)
    return logger

def loadJson(filePath):
    with open(filePath) as fileData:
        fileJson = json.load(fileData)
        return fileJson