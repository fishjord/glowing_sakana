#!/usr/bin/env python
from Bio import SeqIO
import sys

def unroll(infile):
	print "# STOCKHOLM 1.0\n"

	for seq in SeqIO.parse(open(infile), "stockholm"):
		print seq.id.ljust(25), seq.seq

	print "//"	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "USAGE unroll_stk.py <infile>"
	else:
		unroll(sys.argv[1])
