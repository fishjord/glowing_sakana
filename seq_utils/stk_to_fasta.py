#!/usr/bin/python
from Bio import SeqIO
import sys

def convert(infile):
	for seq in SeqIO.parse(open(infile), "stockholm"):
		sys.stdout.write(">%s\n%s\n" %  (seq.id, seq.seq))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "USAGE stk_to_fasta.py <infile>"
	else:
		convert(sys.argv[1])
