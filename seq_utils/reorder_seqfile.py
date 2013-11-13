#!/usr/bin/env python

import sys
from Bio import SeqIO

if len(sys.argv) != 3:
	print "USAGE: reorder_seqfile.py <seq_file> <ordering>"
	sys.exit(1)

seq_map = SeqIO.to_dict(SeqIO.parse(open(sys.argv[1]), "fasta"))


for line in open(sys.argv[2]):
	line = line.strip()

	if line == "":
		continue

	seq = seq_map[line]
	print ">%s\n%s" % (seq.id, seq.seq)

