#!/usr/bin/env python

import sys

if len(sys.argv) != 3:
    print "USAGE: trunc_starts.py <starts_file> <new_k>"
    sys.exit(1)

new_k = int(sys.argv[2])

for line in open(sys.argv[1]):
    lexemes = line.strip().split()

    if len(lexemes) < 4:
        continue

    try:
        int(lexemes[3])
        idx = 2
    except:
        idx = 1

    kmer = lexemes[idx]
    submer = kmer[-new_k:]

    print "%s\t%s\t%s" % ("\t".join(lexemes[:idx]), submer, "\t".join(lexemes[idx+1:]))
