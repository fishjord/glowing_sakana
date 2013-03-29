#!/usr/bin/python

from Bio import SeqIO
import sys

if len(sys.argv) != 2:
    print "USAGE: rename_seqs.py <seq_in>"
    sys.exit(1)

seen = set()
for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    seqid = seq.id
    i = 0

    while seqid in seen:
        seqid = "%s_%s" % (seq.id, i)
        i += 1

    seen.add(seqid)

    print ">%s\n%s" % (seqid, seq.seq)
