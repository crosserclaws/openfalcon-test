#!/usr/bin/env python3

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
    kwargs = smtpCfg['httpApi']['sendMail']
    httpClient = PyHttp(host, smtpCfg['http'], logger)
    
    r = httpClient.call(payload=tCase['data'], **kwargs)
    expt = tCase['expect']
    real = r.text
    assert expt == real