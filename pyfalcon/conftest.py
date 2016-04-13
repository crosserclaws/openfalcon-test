#!/usr/bin/env python3
""" Project level config of pytest. """

import logging
import pytest
from pyutil import pytool

def loadCfg(cfgName):
    return pytool.loadJson(pytool.CONFIG_DIR + cfgName + '.json')

@pytest.fixture(scope="module")
def logger(request):
    verbose = request.config.getoption("-v")
    _logger = pytool.newLogger(request.module.__name__)
    logLevel = logging.DEBUG if verbose else logging.WARNING
    _logger.setLevel(logLevel)
    return _logger

###
# Custom marker and command line option
###

def pytest_addoption(parser):
    parser.addoption("--dev", action="store_true",
        help="Use the value in dev.json to override the value in each module with same key. For example: 'host' value.")

def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers",
        "env(name): mark test to run only on named environment")

def pytest_runtest_setup(item):
    log = logging.getLogger()
    env = "dev" if item.config.getoption("--dev") else "glob"
    envmarker = item.get_marker("env")
    if envmarker is not None:
        envname = envmarker.args[0]
        if envname != env:
            pytest.skip("test requires env %r" % envname)

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
def graphCfg():
    return loadCfg('graph')

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