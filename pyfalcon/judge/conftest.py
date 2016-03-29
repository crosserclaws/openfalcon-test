#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg):
    gHost = gCfg.get('host', None)
    host = gHost if gHost else judgeCfg['host']
    return host