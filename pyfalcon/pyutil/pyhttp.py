#!/usr/bin/env python3
""" HTTP Client of Pyfalcon. """

import logging
import requests

class PyHttp(object):
    """ HTTP Client of Pyfalcon.
    
    :param str host: Server's IP.
    :param str port: Server's port.
    :raises: Exception.
    """
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.addr = 'http://{:s}:{:d}'.format(host, port)
        
    def call(self, api, payload=None, method='GET', needLogin=False, loggerName=None):
        """ Send a HTTP call.
        
        :param str api: API of the HTTP request.
        :param dict payload: Payload of the HTTP request.
        :param str method: HTTP method, either 'GET' or 'POST'.
        :param bool needLogin: If the API needs login session.
        :returns: Response of the HTTP request.
        :rtype: requests.Response.
        """
        
        r = None
        url = self.addr + api
        cookies = self.cookies if needLogin else None
        logger = logging.getLogger(loggerName)
        
        if method == 'GET':
            logger.debug('[GET.][REQ->] %s\n%s', url, payload)
            r = requests.get(url, params=payload, cookies=cookies)
        elif method == 'POST':
            logger.debug('[POST][REQ->] %s\n%s', url, payload)
            r = requests.post(url, data=payload, cookies=cookies)
        else:
            raise Exception('Invalid call argument.')
        
        msg = "[HTTP][RES<-] {:s}\n{:d} {:s}".format(url, r.status_code, r.text)
        logger.debug(msg)
        self.checkResp(r, msg)
        return r
        
    def checkResp(self, resp, msg):
        """ If the HTTP status code is not 200, raise an Exception.
        
        :param requests.Response resp: The response of a HTTP call.
        :raises: Exception.
        """
        
        if resp.status_code != 200:
            raise Exception(msg)
    
    def keepLoginInfo(self, loginDic):
        """ Keep the login session info.
        
        :param dict loginDic: Info for getting login session.
        """
        msg = 'Login Error.'
        r = requests.post(loginDic['url'], data=loginDic['auth'])
        self.checkResp(r, msg)
        
        session = r.cookies.get('sig', None)
        if session is None: raise Exception(msg)
        self.cookies = {'sig': session}