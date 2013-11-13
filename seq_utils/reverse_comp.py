#!/usr/bin/env python

import sys
from Bio import SeqIO

if len(sys.argv) != 2:
	print "USAGE: reverse_comp.py <seqfile>"
	sys.exit(1)

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
	print ">%s" % seq.id
	print seq.seq.reverse_complement()
