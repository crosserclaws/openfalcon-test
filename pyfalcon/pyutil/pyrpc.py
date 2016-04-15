#!/usr/bin/env python3
""" RPC Client of Pyfalcon. """

import json
import socket
import logging
import itertools

class PyRpc(object):
    """ RPC Client of Pyfalcon.
    
    :param str host: Server's IP.
    :param str port: Server's port.
    :param logging.Logger logger: A logger for client to do logging.
    :raises: Exception.
    """
    
    _bufSize = 4096

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._createSuccess = True
        self._id_iter = itertools.count()
        # Socket
        try:
            self._socket = socket.create_connection((host, port))
        except Exception as e:
            self._createSuccess = False
            raise

    def __del__(self):
        if self._createSuccess:
            self._socket.close()

    def call(self, name, *params, loggerName=None):
        """ Send a RPC call.
        
        :param str name: Method name of the RPC call.
        :param params: Arbitrary Argument Lists.
        :returns: Response in json or, empty string if receive an empty response.
        :rtype: json or str('').
        """
        
        req = {
            'id': next(self._id_iter),
            'params': list(params),
            'method': name
        }
        msg = json.dumps(req)
        logger = logging.getLogger(loggerName)
        
        logger.debug("[REQ->] %s\n%s", name, msg)
        self._socket.sendall(msg.encode())

        # Need to receive multiple times if resp is bigger than buffer size.
        resp = self._socket.recv(PyRpc._bufSize)
        if not resp:
            logger.debug("[RES<-] %s\n''(Empty_Response)", name)
            return resp.decode()
        
        resp = json.loads(resp.decode())
        logger.debug("[RES<-] %s\n%s", name, resp)
        self.checkResp(resp, req.get('id'))
        return resp
    
    def checkResp(self, resp, reqId):
        """ Check the value of 'id' and 'error' in resp.
        Raise an Exception when either one of them is abnormal.
        
        :param dict resp: Response in json.
        :param int reqId: Request ID.
        :raises: Exception.
        """
        respId, respErr = resp.get('id'), resp.get('error')
        if respId != reqId:
            raise Exception('[ReqID=%s, ResID=%s] Error: %s'
                            % (reqId, respId, respErr))
        if respErr is not None:
            raise Exception(respErr)

def main():
    """ Self-testing. """
    import time
    rpc = PyRpc("10.20.30.40", 8433)
    for i in range(5):
        mv1 = dict(endpoint='fake-agent', metric='cpu.idle', value=i, step=60,
            counterType='GAUGE', tags='module=transfer-fake', timestamp=int(time.time()))
        mv2 = dict(endpoint='host.test', metric='metric.test.2', value=i, step=60,
            counterType='COUNTER', tags='tag=t'+str(i), timestamp=int(time.time()))
        print( rpc.call("Transfer.Update", [mv1, mv2]) )
        time.sleep(60)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))