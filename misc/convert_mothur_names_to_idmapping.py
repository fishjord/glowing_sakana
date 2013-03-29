#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: mother_names_to_idmapping.py <names file>"
    sys.exit(1)

id = 0
out = open("%s_idmapping.txt" % sys.argv[1], "w")
for line in open(sys.argv[1]):
    lexemes = line.split()
    if len(lexemes) != 2:
        print >>sys.stderr, "achtung, achtung, danger, danger"
        
    out.write("%s\t%s\n" % (id, lexemes[1]))
    id += 1
    
