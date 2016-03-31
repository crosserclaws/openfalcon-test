#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg, judgeCfg):
    dev = request.config.getoption("--dev")
    host = gCfg['host'] if dev else judgeCfg['host']
    return host