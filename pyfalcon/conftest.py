#!/usr/bin/env python3

import logging
import pytest
from pyutil import pytool

def loadCfg(cfgName):
    return pytool.loadJson(pytool.CONFIG_DIR + cfgName + '.json')

@pytest.fixture(scope="module")
def logger(request):
    verbose = request.config.getoption("-v")
    _logger = pytool.newLogger(request.module.__name__)
    _logger.setLevel(logging.DEBUG)
    return _logger

def pytest_addoption(parser):
    parser.addoption("--dev", action="store_true",
        help="Use the value in dev.json to override the value in each module with same key. For example: 'host' value.")

###
# Config
###

@pytest.fixture(scope="session")    
def gCfg(request):
    dev = request.config.getoption("--dev")
    return loadCfg('dev') if dev else loadCfg('global')

@pytest.fixture(scope="session")
def alarmCfg():
    return loadCfg('alarm')

@pytest.fixture(scope="session")
def feCfg():
    return loadCfg('fe')

@pytest.fixture(scope="session")
def hbsCfg():
    return loadCfg('hbs')

@pytest.fixture(scope="session")
def judgeCfg():
    return loadCfg('judge')

@pytest.fixture(scope="session")
def smtpCfg():
    return loadCfg('smtp')

@pytest.fixture(scope="session")
def transferCfg():
    return loadCfg('transfer')