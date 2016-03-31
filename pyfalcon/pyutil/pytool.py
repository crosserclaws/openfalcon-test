#!/usr/bin/env python3

import os
import json
import logging

LOG_FORMAT = '[%(name)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'
logLevel = logging.DEBUG


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

    # def __init__(self, magicOpt, loggerName, cfgFileName, suiteFileName):
    #     # Args
    #     self._optDic = docopt(magicOpt)
    #     # Logger
    #     self.logger = loggerName
    #     # self.logger.setLevel(self._args.loglevel)
    #     return
    #     # Files
    #     self._cfg = self.loadJson(cfgFileName)
    #     self._suite = self.loadJson(suiteFileName)
            
    # @property
    # def logger(self):
    #     print("log getter")
    #     return self._logger
    
    # @logger.setter
    # def logger(self, loggerName=None):
    #     print("log setter")
    #     self._logger = logging.getLogger(loggerName)
    #     handler = logging.StreamHandler()
    #     handler.setLevel(logLevel)
    #     formatter = logging.Formatter(logFormat)
    #     handler.setFormatter(formatter)
    #     self.logger.addHandler(handler)
    
    # def loadJson(self, filePath):
    #     self.logger.info("[FILE.] %s", filePath)
    #     with open(filePath) as fileData:
    #         fileJson = json.load(fileData)
    #         self.logger.debug("[JSON.] %s", fileJson)
    #         return fileJson
        

### 
#  Exp
###

# print(os.path.dirname(__file__))
