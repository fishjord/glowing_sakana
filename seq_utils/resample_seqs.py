#!/usr/bin/env python

import sys
import random
from Bio import SeqIO

if len(sys.argv) != 3:
	print "USAGE: resample_seqs.py <seq_file> <probability>"
	sys.exit(1)

prob = float(sys.argv[2])
in_seqs = 0
out_seqs = 0

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
	in_seqs += 1
	if random.random() < prob:
		out_seqs += 1
		print ">%s\n%s" % (seq.description, seq.seq)

print >>sys.stderr, "Read in %s sequences wrote out %s sequences (%s%%), resampling probability %s%%" % (in_seqs, out_seqs, (float(out_seqs) / in_seqs) * 100, prob * 100)
