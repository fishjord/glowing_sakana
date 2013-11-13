#!/usr/bin/env python

import os
import sys
import struct

if len(sys.argv) != 3:
	print "USAGE: check_nonoverlap.py <nonoverlap.bin> <id_mapping>"
	sys.exit(1)

id_map = dict()

for line in open(sys.argv[2]):
        line = line.strip().strip()
        int_id = line.split()[0]
        exemplar_id = line.split()[1].split(",")[0]

        id_map[int(int_id)] = exemplar_id

f = open(sys.argv[1], "rb")

val = f.read(4)
counts = dict()

while val:
	seqid = struct.unpack(">i", val)[0]
	counts[seqid] = counts.get(seqid, 0) + 1
	val = f.read(4)

for seqid in counts.keys():
	print "%s\t%s\t%s" % (counts[seqid], seqid, id_map[seqid])
