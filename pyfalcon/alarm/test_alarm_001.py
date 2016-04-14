#!/usr/bin/env python3
""" Functional test of HTTP: alarm/event. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {},
        "expect":[],
        "assert": "Get incorrect resp with standard req, API may have some problems."
    }
])
def test_getEvent(alarmCfg, alarmHttp, loggerName, tCase):
    """
    Functional test of HTTP: alarm/event which is login needed.
    The function sends a GET request and check the *list* that ``expt <= resp``.
    
    :param dict alarmCfg: Alarm config.
    :param PyHttp alarmHttp: A HTTP client of alarm.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    ==========   ====================================================================
    Case #       Description
    ==========   ====================================================================
    00           Test the api is working normally if receives a expcted data format.
    ==========   ====================================================================
    """
    
    kwargs = alarmCfg['httpApi']['getEvent']
    
    r = alarmHttp.call(payload=tCase['data'], **kwargs, loggerName=loggerName)
    expt = tCase['expect']
    real = r.json()
    assert expt <= real, tCase['assert']