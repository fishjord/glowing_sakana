#!/usr/bin/env python

import sys
from Bio import SeqIO

if len(sys.argv) != 3:
    print >>sys.stderr, "update_seq_desc.py <input_fasta> <mapping>"
    sys.exit(1)

accno_to_name = {}
for line in open(sys.argv[2]):
    lexemes = line.strip().split("\t")
    if len(lexemes) == 2:
        accno_to_name[lexemes[0]] = lexemes[1]

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    print ">%s %s\n%s" % (seq.id, accno_to_name[seq.id], seq.seq)
