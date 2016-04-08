#!/usr/bin/env python3
""" Functional test of RPC: Hbs.GetStrategies. """

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
    """
    Functional test of RPC: Hbs.GetStrategies.
    The function sends a RPC request and check the *dict* that ``expt <= resp``.
    
    :param dict gCfg: Global config in json.
    :param dict hbsCfg: Hbs config in json.
    :param str host: Host IP to send the request.
    :param logger logger: A logger named in the module's name.
    :param dict tetstCase: A test case in json.
    """
    
    api = hbsCfg['rpcApi']['getStrategies']
    rpcClient = PyRpc(host, hbsCfg['rpc'], logger)
    
    r = rpcClient.call(api, tCase['data'])
    expt = tCase['expect']
    real = r.get('result')
    assert expt.items() <= real.items() 