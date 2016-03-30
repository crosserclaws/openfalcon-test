#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg, transferCfg):
    gHost = gCfg.get('host', None)
    host = gHost if gHost else transferCfg['host']
    return host