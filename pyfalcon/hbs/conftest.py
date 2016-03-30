#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg, hbsCfg):
    gHost = gCfg.get('host', None)
    host = gHost if gHost else hbsCfg['host']
    return host