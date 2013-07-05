#!/usr/bin/env python

from Bio import SeqIO
import sys
import re

seen = set()

def main(accno_file, mode, seq_file_name):
	keep_seqs = set()
	for line in open(accno_file):
		line = line.strip()
		keep_seqs.add(line)

	for seq in SeqIO.parse(open(seq_file_name), "fasta"):
		if mode == "keep" and not seq.id in keep_seqs:
			continue
		elif mode == "remove" and seq.id in keep_seqs:
			continue

		if not seq.id in seen:
			print ">" + seq.id
			print str(seq.seq)
			seen.add(seq.id)

	for id in keep_seqs:
		if id not in seen:
			sys.stderr.write("Didn't see %s\n" % id)

if __name__ == "__main__":
	if len(sys.argv) != 4 or not (sys.argv[2] == "keep" or sys.argv[2] == "remove"):
		print "USAGE: find_seqs.py <accno_list> [keep|remove] <seq_file>"
	else:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
