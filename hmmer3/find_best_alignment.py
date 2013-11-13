#!/usr/bin/env python

from Bio import SeqIO
import sys
import re

regex = re.compile("[^A-Z]")

if len(sys.argv) != 2:
	print "USAGE: find_best_alignment.py <infile>"
	sys.exit(1)

seqs = list(SeqIO.parse(open(sys.argv[1]), "fasta"))
for i in range(0, len(seqs), 6):
	if i+6 >len(seqs):
		break

	frames = seqs[i:i + 6]
	best_seq = None
	best_length = 0

	for frame in frames:
		seq_str = regex.sub("", str(frame.seq))
		if len(seq_str) > best_length:
			best_length = len(seq_str)
			best_seq = frame

	print ">%s\n%s" % (best_seq.id, best_seq.seq)
	
print ">%s\n%s" % (seqs[-1].id, seqs[-1].seq)
