#!/usr/bin/env python3

from pyutil import common
from pyutil import rpcclient as rc

_SUITE_NAME = 'hbs_00'
_SUITE_DESC = 'RPC of Hbs.GetStrategies. (Act like a fake-judge.)'

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
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, testRpcHbsGetStrategies, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
