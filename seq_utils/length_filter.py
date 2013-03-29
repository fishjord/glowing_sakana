#!/usr/bin/python

from Bio import SeqIO
import sys
import os

if len(sys.argv) != 3 and len(sys.argv) != 4:
	print "USAGE: avg_lengths.py <infile> <min_length> [max_length]"
	sys.exit(1)

min_length = int(sys.argv[2])

if len(sys.argv) == 4:
	max_length = int(sys.argv[3])
else:
	max_length = 10000000

passed = 0
total = 0
for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
	total += 1
	l = len(seq.seq)
	if l >= min_length and l <= max_length:
		passed += 1
		print ">%s\n%s" % (seq.description, seq.seq)

print >>sys.stderr, "%s/%s sequences have length >= %s (%s%%)" % (passed, total, min_length, int(passed * 100 / total))
