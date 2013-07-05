#!/usr/bin/python

import sys
from Bio import SeqIO

if len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: convert_seq_case.py <upper|lower> <seqfile>"
    sys.exit(1)

if sys.argv[1] == "upper":
    to_upper = True
elif sys.argv[1] == "lower":
    to_upper = False
else:
    print >>sys.stderr, "Case must be either 'upper' or 'lower'"
    sys.exit(1)

for seq in SeqIO.parse(open(sys.argv[2]), "fasta"):
    if to_upper:
        seqstr = str(seq.seq).upper()
    else:
        seqstr = str(seq.seq).lower()

    print ">{0}\n{1}".format(seq.id, seqstr)
