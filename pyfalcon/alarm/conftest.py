#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg, alarmCfg):
    dev = request.config.getoption("--dev")
    host = gCfg['host'] if dev else alarmCfg['host']
    return host