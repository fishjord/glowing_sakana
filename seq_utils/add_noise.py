#!/usr/bin/python

import sys
import random
from Bio import SeqIO

bases = ['a', 'c', 't', 'g']

def main(in_fasta, rate):
	for seq in SeqIO.parse(open(in_fasta), "fasta"):
		seq_str = str(seq.seq)
		new_seq_str = ""

		for base in seq_str:
			if random.random() > rate:
				new_seq_str = new_seq_str + base
			else:
				new_seq_str = new_seq_str + random.choice(bases)

		print ">%s" % seq.id
		print new_seq_str	

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "USAGE: add_noise.py <in_fasta> <substitution_rate>"
	else:
		main(sys.argv[1], float(sys.argv[2]))
