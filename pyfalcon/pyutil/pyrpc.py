#!/usr/bin/env python3

import json
import socket
import itertools

class PyRpc(object):
    _bufSize = 4096

    def __init__(self, host, port, logger):
        self._createSuccess = True
        self._id_iter = itertools.count()
        # Socket
        try:
            self._socket = socket.create_connection((host, port))
        except Exception as e:
            self._createSuccess = False
            raise
        # Logger
        if logger is not None:
            self.logger = logger
        else:
            raise Exception('Invalid logger argument.')

    def __del__(self):
        if self._createSuccess:
            self._socket.close()

    def call(self, name, *params):
        req = {
            'id': next(self._id_iter),
            'params': list(params),
            'method': name
        }

        msg = json.dumps(req)
        self.logger.debug("[REQ->]\n%s", msg)
        self._socket.sendall(msg.encode())

        # This must loop if resp is bigger than buffer size
        resp = self._socket.recv(PyRpc._bufSize)
        if not resp:
            self.logger.debug("[RES<-] ''(Empty_Response)")
            return resp.decode()
        
        resp = json.loads(resp.decode())
        self.logger.debug("[RES<-]\n%s", resp)
        self.checkResp(resp, req.get('id'))
        return resp
    
    def checkResp(self, resp, reqId):
        """ Check 'id' and 'error' in resp. """
        respId, respErr = resp.get('id'), resp.get('error')
        if respId != reqId:
            raise Exception('[ReqID=%s, ResID=%s] Error: %s'
                            % (reqId, respId, respErr))
        if respErr is not None:
            raise Exception(respErr)

def main():
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
