#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg, graphCfg):
    dev = request.config.getoption("--dev")
    host = gCfg['host'] if dev else graphCfg['host']
    return host