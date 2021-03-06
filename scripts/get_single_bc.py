#!/usr/bin/env python

import os
import re
import sys

default_fname = "s2e-last/debug.txt"

p_on_block_end = re.compile("onTranslateBlockEnd\. endPc = (0x[a-fA-F0-9]{16}), targetPc = (0x[a-fA-F0-9]{16})\.")
#p_covered_branch = re.compile("(0x[a-fA-F0-9]{1,16}) -> (0x[a-fA-F0-9]{16}): \d+")
p_covered_branch = re.compile("execute edge pc = (0x[a-fA-F0-9]{1,16}), next pc = (0x[a-fA-F0-9]{16})")

all_branches = {}
covered_branches = {}

fname = default_fname

if len(sys.argv) > 1:
    fname = sys.argv[1]

f = open(fname, 'r')

for line in f:
    m = p_on_block_end.search(line)
    if m:
        src = m.group(1)
        dst = m.group(2)
        all_branches[src + ':' + dst] = True
        continue

    m = p_covered_branch.search(line)
    if m:
        src = m.group(1)
        dst = m.group(2)
        covered_branches[src + ':' + dst] = True
        continue

f.close()

print(all_branches)
print("---------------------")
print(covered_branches)

for edge in covered_branches:
    if edge not in all_branches:
        src,dst = edge.split(':')
        print("%s not in all_branches." % edge)

print("Coverage rage: %f (%d/%d)" % (float(len(covered_branches)) / float(len(all_branches)), len(covered_branches), len(all_branches)))

"""
for edge in all_branches:
    if edge not in covered_branches:
        src,dst = edge.split(':')
        print("%s is not covered." % edge)
"""

#import pdb
#pdb.set_trace()


