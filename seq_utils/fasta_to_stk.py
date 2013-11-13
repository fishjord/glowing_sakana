#!/usr/bin/env python

from Bio import AlignIO
import sys

def convert(infile):
	input_handle = open(infile, "rU")
	
	alignments = AlignIO.parse(input_handle, "fasta")
	AlignIO.write(alignments, sys.stdout, "stockholm")
 
	input_handle.close()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "USAGE fasta_to_stk.py <infile>"
	else:
		convert(sys.argv[1])
