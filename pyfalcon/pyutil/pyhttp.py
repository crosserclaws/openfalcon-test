#!/usr/bin/env python3

import requests

class PyHttp(object):
    
    def __init__(self, host, port, logger):
        self.addr = 'http://{:s}:{:d}'.format(host, port)
        # Logger
        if logger is not None:
            self.logger = logger
        else:
            raise Exception('Invalid logger argument.')
        
    def call(self, api, payload=None, method='GET', needLogin=False):
        r = None
        url = self.addr + api
        cookies = self.cookies if needLogin else None
        
        if method == 'GET':
            self.logger.debug('[GET.][REQ->]\n%s', payload)
            r = requests.get(url, params=payload, cookies=cookies)
        elif method == 'POST':
            self.logger.debug('[POST][REQ->]\n%s', payload)
            r = requests.post(url, data=payload, cookies=cookies)
        else:
            raise Exception('Invalid call argument.')
        
        self.checkResp(r)
        return r
        
    def checkResp(self, resp):
        """ Raise Exception if the HTTP status code is not 200. """
        msg = "[HTTP.] {:d} {:s}".format(resp.status_code, resp.text)
        if resp.status_code == 200:
            self.logger.debug(msg)
        else:
            raise Exception(msg)
    
    def keepLoginInfo(self, loginDic):
        """ Keep the login session info. """
        r = requests.post(loginDic['url'], data=loginDic['auth'])
        self.checkResp(r)
        
        session = r.cookies['sig']
        self.cookies = {'sig': session}
        self.logger.debug("[SIG.] %s", session)