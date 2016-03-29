#!/usr/bin/env python3

import pytest
from pyutil.pyrpc import PyRpc

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
        },
        "expect": {
        }
    }
])
def test_getStrategies(gCfg, hbsCfg, host, logger, tCase):
    api = hbsCfg['rpcApi']['getStrategies']
    rpcClient = PyRpc(host, hbsCfg['rpc'], logger)
    
    r = rpcClient.call(api, tCase['data'])
    expt = tCase['expect']
    real = r.get('result')
    assert expt.items() <= real.items() 