#!/usr/bin/env python3

import pytest

@pytest.fixture(scope="session")
def host(request, gCfg, alarmCfg):
    gHost = gCfg.get('host', None)
    host = gHost if gHost else alarmCfg['host']
    return host