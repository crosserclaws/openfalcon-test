#!/usr/bin/env python3

from pyutil import common
from pyutil import rpcclient as rc

_suiteName = 'transfer_00'
_suiteDesc = 'RPC of Transfer.Update. (Act like a fake-agent.)'

def testRpcTransferUpdate(logger, tCase, cfg):
    # Arrange & Act
    mv = tCase['data']['payload']
    expect = tCase['expect']['payload']
    rpc = rc.RpcClient((cfg['host'], cfg['rpc']), logger)
    real = rpc.call("Transfer.Update", mv)
    
    # Assert
    onePass = True
    logger.debug("[DATA.] %s ?<= %s", expect, real)
    diffkeys = [k for k in expect if expect[k] != real[k]]
    if diffkeys:
        onePass = False
    return onePass

def main():
    logger, cfg, suite = common.init(_suiteName, common.gCfgName, _suiteName + '.json')
    common.runTestSuite(_suiteName, testRpcTransferUpdate, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
