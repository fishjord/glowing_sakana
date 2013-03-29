#!/usr/bin/python

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys
import os

def main(seq_file, region_start, region_end, format):
	out_seqs = []
	for seq in SeqIO.parse(open(seq_file), format):
		seq_start = -1
		seq_end = 0
		
		for i in range(len(seq.seq)):
			if str(seq.seq[i]).isupper():
				if seq_start == -1:
					seq_start = i
				seq_end = i + 1

		if region_start >= seq_start and region_end <= seq_end:
			out_seqs.append(SeqRecord(seq.seq[region_start:region_end], seq.id, "", ""))
#			sys.stdout.write(">%s\n%s\n" % (seq.description, seq.seq[region_start:region_end]))
		else:
			sys.stderr.write("%s\t%d\t%d\tDoesn't cover region\n" % (seq.id, seq_start, seq_end))

	SeqIO.write(out_seqs, sys.stdout, format)

if __name__ == "__main__":
	if len(sys.argv) != 4 and len(sys.argv) != 5:
		print "USAGE: seq_trimmer.py <seq_file> <region_start> <region_end>"
	else:
		format = "fasta"

		if len(sys.argv) == 5:
			format = sys.argv[4]

		main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), format)
