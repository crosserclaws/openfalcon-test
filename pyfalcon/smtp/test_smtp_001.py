#!/usr/bin/env python3
""" Functional test of HTTP: smtp/mail. """

import pytest

@pytest.mark.parametrize("tCase", [
    {
        "number": "00",
        "data": {
            "tos": "cheminlin@cepave.com,,",
            "subject": "fake-subject_00",
            "content": "fake-content_00."
        },
        "expect": "Success.",
        "assert": "Mail with valid data but get unexpected msg."
    },
    {
        "number": "01",
        "data": {
            "tos": ",cheminlin@cepave.com,",
            "subject": "fake-subject_01",
            "content": "fake-content_01."
        },
        "expect": "Success.",
        "assert": "Mail with acceptably invalid data but get unexpected msg."
    }
])
def test_sendMail(smtpCfg, smtpHttp, loggerName, tCase):
    """
    Functional test of HTTP: smtp/mail.
    Send a POST request and test the resp string.
    
    :param dict smtpCfg: Smtp config.
    :param PyHttp smtpHttp: A HTTP client of smtp.
    :param str loggerName: Used for getting the custom logger.
    :param dict tCase: Data of a test case.
    
    ==========   ==============================================================
    Case #       Description
    ==========   ==============================================================
    00           Mail with valid data to test if it is working normally.
    01           Mail with acceptably invalid data to test if it is working normally.
    ==========   ==============================================================
    """
    
    kwargs = smtpCfg['httpApi']['sendMail']
    
    r = smtpHttp.call(payload=tCase['data'], **kwargs, loggerName=loggerName)
    expt = tCase['expect']
    real = r.text
    assert expt == real, tCase['assert']