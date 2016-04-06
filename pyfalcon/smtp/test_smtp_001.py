#!/usr/bin/env python3
"""
Functional test of smtp HTTP: /mail.
"""

import pytest
from pyutil.pyhttp import PyHttp

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
            "tos": "cheminlin@cepave.com,,",
            "subject": "fake-subject_00",
            "content": "fake-content_00."
        },
        "expect": "Success."
    },
    {
        "number": "01",
        "data": {
            "tos": ",cheminlin@cepave.com,",
            "subject": "fake-subject_01",
            "content": "fake-content_01."
        },
        "expect": "Success."
    }
])
def test_sendMail(gCfg, smtpCfg, host, logger, tCase):
    """
    Functional test of smtp HTTP: /mail.
    The function sends a POST request and check if resp is ``Success.``.
    
    :param dict gCfg: Global config in json.
    :param dict alarmCfg: Smtp config in json.
    :param str host: Host IP to send the request.
    :param logger logger: A logger named in the module's name.
    :param dict tetstCase: A test case in json.
    """
    kwargs = smtpCfg['httpApi']['sendMail']
    httpClient = PyHttp(host, smtpCfg['http'], logger)
    
    r = httpClient.call(payload=tCase['data'], **kwargs)
    expt = tCase['expect']
    real = r.text
    assert expt == real