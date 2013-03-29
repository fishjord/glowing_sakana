#!/usr/bin/python

from Bio import SeqIO
import sys

if len(sys.argv) != 2:
	print "USAGE: dealign.py <seq_file>"
	sys.exit(1)

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
	if str(seq.id)[0] == '#':
		continue

	print ">%s" % (seq.description)
	print str(seq.seq).replace("-", "").replace(".", "").lower()
