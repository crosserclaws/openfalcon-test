#!/usr/bin/env python3
""" Filter pytest's output for simplified info.
Usage: py.test --tb=no | ./filter.py
"""

import re
import sys

def main():
    pCount, fCount = 0, 0
    pattern = re.compile(r'[a-z]+/test_(\w+).py ([.xsFE]+)')

    for line in sys.stdin:
        m = pattern.match(line)
        if not m:
            continue
        
        msg = 'Pass'
        PASS_STR = '.sx'
        outFormat = '{:<15s}   {:s}'
        case, result = m.groups()
        for c in result:
            if c not in PASS_STR:
                msg = 'Fail'
                fCount += 1
                break
        if msg == 'Pass': pCount += 1
        print(outFormat.format(case, msg))

    print()
    print('Summary: %d Pass, %d Fail, %d Total' %(pCount, fCount, pCount+fCount))

if __name__ == "__main__":
    sys.exit(int(main() or 0))