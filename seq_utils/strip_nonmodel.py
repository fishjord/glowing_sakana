#!/usr/bin/env python

import sys
import re
from Bio import SeqIO

if len(sys.argv) != 2:
	print "USAGE: strip_nonmodel.py <infile>"
	sys.exit(1)

nonmodel_regex = re.compile("[^A-Z\-]")

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
	print ">%s\n%s" % (seq.description, nonmodel_regex.sub("", str(seq.seq)))
