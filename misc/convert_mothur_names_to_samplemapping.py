#!/usr/bin/python

import sys
import os

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: mother_names_to_samplemapping.py <names file>"
    sys.exit(1)

fname = os.path.split(sys.argv[1])[-1]
if "." in fname:
    fname = fname[:fname.rfind(".")]

out = open("%s_sample_mapping.txt" % sys.argv[1], "w")
for line in open(sys.argv[1]):
    lexemes = line.split()
    if len(lexemes) != 2:
        print >>sys.stderr, "achtung, achtung, danger, danger"

    for seq in lexemes[1].split(","):
        out.write("%s\t%s\n" % (seq, fname))

    
