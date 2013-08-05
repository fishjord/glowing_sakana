#!/usr/bin/python

from Bio import SeqIO
import sys

if len(sys.argv) != 2:
    print "USAGE: rename_seqs.py <seq_in>"
    sys.exit(1)

seen = set()
for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    seqid = seq.id
    desc = seq.description.split(" ")
    desc = " ".join(desc[1:])
    i = 0

    while seqid in seen:
        seqid = "%s_%s" % (seq.id, i)
        i += 1

    seen.add(seqid)

    print ">{0} {1}\n{2}".format(seqid, desc, seq.seq)
