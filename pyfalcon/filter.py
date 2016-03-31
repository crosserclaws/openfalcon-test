#!/usr/bin/env python3

import re
import sys

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