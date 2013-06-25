#!/usr/bin/python

from Bio import SeqIO
import re
import sys

def main(seq_file_name):
	sys.stderr.write("Processing " +  seq_file_name + " writing good seqs to stdout\n")

	good_seq_regex = re.compile("^[A-Za-z]+$")
	seqs_read = 0
	seqs_written = 0

	for seq in SeqIO.parse(open(seq_file_name, "r"), "fasta"):
		seqs_read = seqs_read + 1
		if good_seq_regex.match(str(seq.seq)):
			print ">" + seq.id + "\n" + str(seq.seq) + "\n"
			seqs_written = seqs_written + 1
		else:
			print >>sys.stderr, "%s" % seq.id

	sys.stderr.write("Processing complete, read " + str( seqs_read) + " wrote " + str( seqs_written) + " sequences\n")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "USAGE: filter_seqs.py input_file"
	else:
		main(sys.argv[1])
