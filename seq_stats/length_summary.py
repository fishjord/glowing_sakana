#!/usr/bin/env python

from Bio import SeqIO
import sys
import os

if len(sys.argv) < 2:
	print "USAGE: avg_lengths.py <infile>..."
	sys.exit(1)

length_map = dict()
for f in sys.argv[1:]:
	length_map[f] = []

	for seq in SeqIO.parse(open(f), "fasta"):
		length_map[f].append(len(seq.seq))

longest_length = 0
for f in length_map:
	sys.stdout.write("%s\t" % os.path.split(f)[1])
	length_map[f] = sorted(length_map[f])
	if len(length_map[f]) > longest_length:
		longest_length = len(length_map[f])

sys.stdout.write("\n")

for i in range(longest_length):
	for l in length_map.values():
		if len(l) > i:
			sys.stdout.write("%s\t" % l[i])
		else:
			sys.stdout.write(" \t")

	sys.stdout.write("\n")
