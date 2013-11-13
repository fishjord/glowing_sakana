#!/usr/bin/env python

import random
import sys

if len(sys.argv) != 2:
    print "USAGE: random_sample.py <in hmmgs>"
    sys.exit(1)

by_ref = {}
header = ""
for line in open(sys.argv[1]):
    if line[0] == "#":
        header = line.strip()
    lexemes = line.strip().split("\t")
    if len(lexemes) < 2:
        continue

    refid = lexemes[2]

    if refid not in by_ref:
        by_ref[refid] = []

    by_ref[refid].append(line.strip())

print header
for refid in by_ref:
    print random.choice(by_ref[refid])
