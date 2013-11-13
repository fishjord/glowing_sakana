#!/usr/bin/env python

import sys
from Bio import SeqIO

if len(sys.argv) != 4:
    print "USAGE: kmer_coverage.py <ref> <query> <k>"
    sys.exit(1)

k = int(sys.argv[3])
ref_kmers = {}

for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    seqstr = str(seq.seq).lower()
    for i in range(1, len(seqstr) - k + 1):
        ref_kmers[seqstr[i:i+k]] = 0

for seq in SeqIO.parse(open(sys.argv[2]), "fasta"):
    seqstr = str(seq.seq).lower()
    for i in range(1, len(seqstr) - k + 1):
        kmer = seqstr[i:i+k]
        if kmer in ref_kmers:
            ref_kmers[kmer] += 1

covered = 0

for kmer in ref_kmers:
    print "%s\t%s" % (kmer, ref_kmers[kmer])
    if ref_kmers[kmer] != 0:
        covered += 1

print >>sys.stderr, "Covered ref kmers: %d/%d (%f)" % (covered, len(ref_kmers), float(covered) * 100 / len(ref_kmers))
