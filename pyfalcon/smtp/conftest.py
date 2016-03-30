#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg, smtpCfg):
    dev = request.config.getoption("--dev")
    host = gCfg['host'] if dev else smtpCfg['host']
    return host