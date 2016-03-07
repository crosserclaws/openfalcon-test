#!/usr/bin/env python3

import time
from pyutil import common
from pyutil import rpcclient as rc

_suiteName = 'transfer_00'
_suiteDesc = 'RPC of Transfer.Update. (Act like a fake-agent.)'

def testRpcTransferUpdate(logger, tCase, cfg, args):
    # Arrange
    onePass = True
    mv = tCase['data']['payload']
    expect = tCase['expect']['payload']
    rpc = rc.RpcClient((cfg['host'], cfg['rpc']), logger)
    # Act
    for idx in range(args.loop):
        real = rpc.call("Transfer.Update", mv)
        # Assert
        logger.debug("[DATA.%02d] %s ?<= %s", idx, expect, real)
        diffkeys = [k for k in expect if expect[k] != real[k]]
        if diffkeys:
            onePass = False
        if args.step > 0:
            time.sleep(args.step)
    return onePass

def setParser(parser):
    parser.add_argument(
        '-l',
        help="Loop times of a rpc call in each test case.",
        action="store", dest="loop", default=1, type=int
    )
    parser.add_argument(
        '-s',
        help="Step time of a rpc call in each test case.",
        action="store", dest="step", default=0, type=int
    )

def main():
    logger, cfg, suite, args = common.init(_suiteName, common.gCfgName, _suiteName + '.json', setParser)
    common.runTestSuite(_suiteName, testRpcTransferUpdate, logger, suite, cfg, args)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
