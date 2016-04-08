#!/usr/bin/env python3
""" Functional test of HTTP: transfer/api/push. """

import json
import pytest
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": [
            {
                "endpoint": "bgp-bj-058-083-161-105",
                "metric": "cpu.idle",
                "value": 0.7857,
                "step": 1,
                "counterType": "COUNTER",
                "tags": "tag",
                "timestamp": 1452493440
            }
        ],
        "expect": {
            "msg": "success",
            "data": {
                "Message": "ok",
                "Total": 1,
                "Invalid": 0,
                "Latency": 0
            }
        }
    }
])
def test_apiPush(gCfg, transferCfg, host, logger, tCase):
    """
    Functional test of HTTP: transfer/api/push.
    The function sends a POST request and check the *dict* that ``expt == real``.
    
    :param dict gCfg: Global config in json.
    :param dict transferCfg: Transfer config in json.
    :param str host: Host IP to send the request.
    :param logger logger: A logger named in the module's name.
    :param dict tetstCase: A test case in json.
    """
    
    kwargs = transferCfg['httpApi']['apiPush']
    httpClient = PyHttp(host, transferCfg['http'], logger)
    
    # Convert list into string for raw payload.
    r = httpClient.call(payload=json.dumps(tCase['data']), **kwargs)
    expt = tCase['expect']
    real = r.json()
    assert expt == real