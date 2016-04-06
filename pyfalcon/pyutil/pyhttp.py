#!/usr/bin/env python3
""" HTTP Client of Pyfalcon. """

import requests

class PyHttp(object):
    """ HTTP Client of Pyfalcon.
    
    :param str host: Server's IP.
    :param str port: Server's port.
    :param logging.Logger logger: A logger for client to do logging.
    :raises: Exception
    """
    
    def __init__(self, host, port, logger):
        self.addr = 'http://{:s}:{:d}'.format(host, port)
        # Logger
        if logger is not None:
            self.logger = logger
        else:
            raise Exception('Invalid logger argument.')
        
    def call(self, api, payload=None, method='GET', needLogin=False):
        """ Send a HTTP call with given arguments.
        
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
        
        if method == 'GET':
            self.logger.debug('[GET.][REQ->] %s\n%s', api, payload)
            r = requests.get(url, params=payload, cookies=cookies)
        elif method == 'POST':
            self.logger.debug('[POST][REQ->] %s\n%s', api, payload)
            r = requests.post(url, data=payload, cookies=cookies)
        else:
            raise Exception('Invalid call argument.')
        
        msg = "[HTTP][RES<-] {:s}\n{:d} {:s}".format(api, r.status_code, r.text)
        self.logger.debug(msg)
        self.checkResp(r)
        return r
        
    def checkResp(self, resp):
        """ If the HTTP status code is not 200, raise an Exception.
        
        :param requests.Response resp: The response of a HTTP call.
        :raises: Exception
        """
        
        if resp.status_code != 200:
            raise Exception(msg)
    
    def keepLoginInfo(self, loginDic):
        """ Keep the login session info.
        
        :param dict loginDic: Info for getting login session.
        """
        r = requests.post(loginDic['url'], data=loginDic['auth'])
        self.checkResp(r)
        
        session = r.cookies['sig']
        self.cookies = {'sig': session}
        self.logger.debug("[SIG.] %s", session)