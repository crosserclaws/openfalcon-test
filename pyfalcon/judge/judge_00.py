#!/usr/bin/env python3

import time
from pyutil import common
from pyutil import rpcclient as rc

_SUITE_NAME = 'judge_00'
_SUITE_DESC = 'RPC of Judge.Send. (Act like a fake-transfer.)'

def testRpcJudgeSend(logger, tCase, cfg):
    # Arrange
    mv = tCase['data']
    rpc = rc.RpcClient((cfg['host'], cfg['rpc']), logger)
    # Act
    _ = rpc.call("Judge.Send", mv)
    return True

def main():
    logger, cfg, suite, _ = common.init(_SUITE_NAME, common.CFG_NAME, _SUITE_NAME + '.json')
    common.runTestSuite(_SUITE_NAME, testRpcJudgeSend, logger, suite, cfg)

if __name__ == "__main__":
    import sys
    sys.exit(int(main() or 0))
