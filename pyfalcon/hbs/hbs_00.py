#!/usr/bin/env python3

from pyutil import common
from pyutil import rpcclient as rc

_SUITE_DESC = 'RPC of Hbs.GetStrategies. (Act like a fake-judge.)'
_SUITE_NAME = common.getFnameWoExt(__file__)
MODULE_PATH = common.getAbsFilePath(__file__)

def testRpcHbsGetStrategies(logger, tCase, cfg):
    # Arrange & Act
    arg = {}
    expect = tCase['expect']
    rpc = rc.RpcClient((cfg['host'], cfg['rpc']), logger)
    real = rpc.call("Hbs.GetStrategies", arg)
    if not expect:
        return True

    # Todo
    # Expect has specified values.
    
    return False

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, MODULE_PATH + common.CFG_NAME, MODULE_PATH + _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, testRpcHbsGetStrategies, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
