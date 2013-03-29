#!/usr/bin/python

import sys
from Bio import SeqIO

if len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: decompose_kmers.py <input_fasta> <k>"
    sys.exit(1)

k = int(sys.argv[2])

kmers = set()
for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    if len(seq) < k:
        print >>sys.stderr, "Skipping %s due to length" % seq.id
    for i in range(len(seq) - k + 1):
        kmers.add(seq.seq[i:i + k])

print >>sys.stderr, "Read in %s %s-mers from %s" % (len(kmers), sys.argv[2], sys.argv[1])

i = 1
for kmer in kmers:
    print ">kmer_%s\n%s" % (i, kmer)
    i += 1
