#!/usr/bin/env python3

import json
import socket
import itertools
from pyutil import common

class RpcClient():
    _bufSize = 4096

    def __init__(self, addr, logger=None):
        self._id_iter = itertools.count()
        # Socket
        try:
            self._socket = socket.create_connection(addr)
        except Exception as e:
            self._createSuccess = False
            raise Exception("%s (@ RpcClient.init())" % e)
        # Logger
        if logger is None:
            self._logger = common.newLogger("RpcClient")
        else:
            self._logger = logger

    def __del__(self):
        if self._createSuccess:
            self._socket.close()

    def call(self, name, *params):
        req = dict(id=next(self._id_iter),
                    params=list(params),
                    method=name)

        msg = json.dumps(req)
        self._logger.debug("[REQ->]\n%s", msg)
        self._socket.sendall(msg.encode())

        # This must loop if resp is bigger than buffer size
        resp = self._socket.recv(self._bufSize)
        resp = json.loads(resp.decode())

        if resp.get('id') != req.get('id'):
            raise Exception("expected id=%s, received id=%s: %s"
                            %(id, resp.get('id'), resp.get('error')))

        if resp.get('error') is not None:
            raise Exception(resp.get('error'))
        
        res = resp.get('result')
        self._logger.debug("[RES<-]\n%s", res)
        return res

def main():
    import time
    rpc = RpcClient(("10.20.30.40", 8433))
    for i in range(2):
        mv1 = dict(endpoint='host.test', metric='metric.test.1', value=i, step=60,
            counterType='GAUGE', tags='tag=t'+str(i), timestamp=int(time.time()))
        mv2 = dict(endpoint='host.test', metric='metric.test.2', value=i, step=60,
            counterType='COUNTER', tags='tag=t'+str(i), timestamp=int(time.time()))
        print( rpc.call("Transfer.Update", [mv1, mv2]) )

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
