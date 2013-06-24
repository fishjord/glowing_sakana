#!/usr/bin/python

import sys
import re
from Bio import SeqIO

if len(sys.argv) != 2:
	print "USAGE: remove_invalid.py <infile>"
	sys.exit(1)

regex = re.compile("[^a-zA-Z]")

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
	seq_str = str(seq.seq)
	final_seqstr = regex.sub("", seq_str)
	if len(final_seqstr) == 0:
		print >>sys.stderr, "{0}\tdropped".format(seq.id)
	else:
		if len(final_seqstr) != len(seq_str):
			print >>sys.stderr, "{0}\t{1}".format(seq.id, seq_str)
		print ">%s\n%s" % (seq.description, regex.sub("", str(seq.seq)))
