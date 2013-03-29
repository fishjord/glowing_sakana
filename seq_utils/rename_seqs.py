#!/usr/bin/python

from Bio import SeqIO
import sys

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print "USAGE: rename_seqs.py <seq_in> [append]"
    sys.exit(1)

append = None
if len(sys.argv) == 3:
    append = sys.argv[2]

i = 0
for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    seqid = seq.id

    if append:
        seqid += "_%s" % append
    else:
        seqid = "%s" % i
        i += 1

    print ">%s\n%s" % (seqid, seq.seq)
