#!/usr/bin/env python

import sys
import numpy

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: mpileup_ref_coverage.py <mpileup.txt> [refseq.fasta]"
    sys.exit(1)

if len(sys.argv) == 3:
    from Bio import SeqIO
    refseq_lengths = {}
    for seq in SeqIO.parse(open(sys.argv[2]), "fasta"):
        refseq_lengths[seq.id] = len(seq.seq)
else:
    refseq_lengths = None

ref_cov = {}
all_cov = []
for line in open(sys.argv[1]):
    lexemes = line.strip().split("\t")
    #contig_17       124     N       1       ^!g     I
    if len(lexemes) != 6:
        continue

    refid = lexemes[0]
    cov = int(lexemes[3])

    if refid not in ref_cov:
        ref_cov[refid] = []

    ref_cov[refid].append(cov)
    all_cov.append(cov)

s = "#refid\tmedian_cov\tmean_cov\tcovered_pos"
if refseq_lengths != None:
    s += "\tcovered_ratio"

print s
for refid in sorted(ref_cov.keys()):
    coverage = ref_cov[refid]
    if refseq_lengths != None:
        uncovered = max(refseq_lengths.get(refid, 0) - len(coverage), 0)
        if uncovered > 0:
            coverage.extend([0] * uncovered)
    else:
        uncovered = 0

    s = "{0}\t{1}\t{2}\t{3}".format(refid, numpy.median(coverage), numpy.mean(coverage), len(coverage) - uncovered)
    if refseq_lengths != None:
        s += "\t{0}".format((len(coverage) - uncovered) / float(len(coverage)))
    print s
