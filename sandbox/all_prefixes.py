#!/usr/bin/python

import sys
from Bio import SeqIO

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: all_prefixes.py <seq_file>"
    sys.exit(1)

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    seqstr = str(seq.seq)
    for i in range(len(seqstr)):
        print ">%s_1-%s\n%s" % (seq.id, i+2, seqstr[:i+1])
