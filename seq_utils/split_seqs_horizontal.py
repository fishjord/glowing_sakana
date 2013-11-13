#!/usr/bin/env python

import sys
from Bio import SeqIO

if len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: split_seqs_horizontal.py <input_fasta> <window>"
    sys.exit(1)

window = int(sys.argv[2])

kmers = set()
for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    for i in range(0, len(seq), window):
        print ">%s_%s\n%s" % (seq.id, i + 1, seq.seq[i:i+window])
