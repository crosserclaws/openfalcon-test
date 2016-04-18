#!/usr/bin/env python3
""" Functional test of RPC: Hbs.GetStrategies. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {},
        "expect": {},
        "assert": "A valid call but receive incorrect resp type, API may have some problems."
    }
])
def test_getStrategies(hbsCfg, hbsRpc, loggerName, tCase):
    """
    Functional test of RPC: Hbs.GetStrategies.
    Send a RPC request and test if expected element is in the resp.
    
    :param dict hbsCfg: Hbs config.
    :param PyHttp hbsRpc: A HTTP client of hbs.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Simply get strategies to test if it is working normally.
    ==========   ==============================================================
    """
    
    api = hbsCfg['rpcApi']['getStrategies']
    
    r = hbsRpc.call(api, tCase['data'], loggerName=loggerName)
    expt = tCase['expect']
    real = r.get('result')
    assert expt.items() <= real.items(), tCase['assert']