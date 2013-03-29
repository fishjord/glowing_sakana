#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print "USAGE: remove_dup_starts.py <starts_file>"
    sys.exit(1)

starts = set()

for line in open(sys.argv[1]):
    lexemes = line.strip().split("\t")
    model_pos = lexemes[-1]
    kmer = lexemes[3]

    key = kmer + "_" + model_pos

    if key in starts:
        continue

    starts.add(key)
    print line.strip()
