#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg, feCfg):
    dev = request.config.getoption("--dev")
    host = gCfg['host'] if dev else feCfg['host']
    return host