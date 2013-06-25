#!/usr/bin/python

import sys
import re
from Bio import SeqIO

if len(sys.argv) != 2:
	print "USAGE: drop_invalid_seqs.py <infile>"
	sys.exit(1)

regex = re.compile("[^a-zA-Z]")

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
	seq_str = str(seq.seq)
	if "[" in seq_str:
		print >>sys.stderr, "Oh noes!"
	else:
		print ">%s\n%s" % (seq.description, seq_str)
