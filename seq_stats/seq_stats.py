#!/usr/bin/python

from Bio import SeqIO
import numpy
import sys
import re

non_model_regex = re.compile("[a-z\.]")

def main(mode, fasta_files):
	num_seqs = 0
	lengths = []

	for fasta_file in fasta_files:
		for seq in SeqIO.parse(open(fasta_file), "fasta"):
			if seq.id[0] == "#":
				continue

			length = 0
			seq_string = str(seq.seq)
			if mode == "model":
				length = len(re.sub(non_model_regex, "", seq_string))
			elif mode == "unaligned":
				length = len(re.sub(r'[\-\.]', "", seq_string))
			elif mode == "model-length":
				start = -1
				end = -1

				seq_string = re.sub(non_model_regex, "", seq_string)
				
				for i in range(0, len(seq_string)):
					if seq_string[i] != "-" and start == -1:
						start = i
					if seq_string[i] != "-" and start != -1:
						end = i

				length = max(0, end - start)
			else:
				length = len(seq_string)

			num_seqs = num_seqs + 1
			lengths.append(length)

	print "Total number of sequenecs %d" % num_seqs
	print "Max length:     %s" % max(lengths)
	print "Min length:     %s" % min(lengths)
	print "Avg length:     %s" % numpy.mean(lengths)
	print "Standard dev:   %s" % numpy.std(lengths)
	print "Median lenght:  %s" % numpy.median(lengths)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "USAGE: calc_avg_length.py [--model-only|--unaligned] <fasta_file>..."
	else:
		if sys.argv[1] == "--model-only":
			main("model", sys.argv[2:])
		elif sys.argv[1] == "--model-length":
			main("model-length", sys.argv[2:])
		elif sys.argv[1] == "--unaligned":
			main("unaligned", sys.argv[2:])
		else:
			main("rawr", sys.argv[1:])
