#!/usr/bin/env python

import sys
import os
from Bio import SeqIO

if len(sys.argv) != 2:
	print "USAGE: reverse_seqs.py <input stockholm file>"
	sys.exit(1)

out_seqs = []
for seq in SeqIO.parse(open(sys.argv[1]), "stockholm"):
	seq.seq = seq.seq[::-1]
	out_seqs.append(seq)

SeqIO.write(out_seqs, open("reversed_%s" % os.path.split(sys.argv[1])[1], "w"), "stockholm")
