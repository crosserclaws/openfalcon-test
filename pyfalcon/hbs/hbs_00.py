#!/usr/bin/env python3

from pyutil import common
from pyutil import rpcclient as rc

_suiteName = 'hbs_00'
_suiteDesc = 'RPC of Hbs.GetStrategies. (Act like a fake-judge.)'

def testRpcHbsGetStrategies(logger, tCase, cfg):
    # Arrange & Act
    arg = {}
    expect = tCase['expect']
    rpc = rc.RpcClient((cfg['host'], cfg['rpc']), logger)
    real = rpc.call("Hbs.GetStrategies", arg)
    if not expect:
        logger.debug(real)
        return True

    # Todo
    # Expect has specified values.
    
    return False

def main():
    logger, cfg, suite, _ = common.init(_suiteName, common.gCfgName, _suiteName + '.json')
    common.runTestSuite(_suiteName, testRpcHbsGetStrategies, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
