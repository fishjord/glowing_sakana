#!/usr/bin/env python

from Bio import SeqIO
import sys

if len(sys.argv) != 3:
    print "USAGE: trunc_seqs.py <seq_file> <length>"
    sys.exit(1)

seq_file = sys.argv[1]
trunc_len = int(sys.argv[2])
f_type = "fasta"
if seq_file.endswith(".fq") or seq_file.endswith(".fastq"):
    f_type = "fastq"

for seq in SeqIO.parse(open(seq_file), f_type):
    seq_str = str(seq.seq)
    trunc_seq = seq_str
    if len(seq_str) < trunc_len:
        print >>sys.stderr, "Seq %s's length (%s) shorter than trunc len (%s)" % (seq.id, len(seq_str), trunc_len)
    else:
        trunc_seq = seq_str[:trunc_len]

    print ">%s\n%s" % (seq.id, trunc_seq)
