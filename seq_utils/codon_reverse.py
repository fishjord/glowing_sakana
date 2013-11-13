#!/usr/bin/env python

from Bio import SeqIO
import sys

if len(sys.argv) != 2:
	print "USAGE: codon_reverse.py <nucl_file>"
	sys.exit(1)

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
	seq_str = str(seq.seq)
	out_seq = ""
	for i in range(len(seq_str), 0, -3):
		start = i - 3
		end = i

		if end >= len(seq_str):
			end = len(seq_str)

		out_seq += seq_str[start:end]

	print ">%s\n%s" % (seq.id, out_seq)
