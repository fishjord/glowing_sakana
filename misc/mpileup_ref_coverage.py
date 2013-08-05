#!/usr/bin/env python

import argparse
import sys
import numpy
from Bio import SeqIO

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--min-median-cov", dest="min_median", default=0, type=int, help="Don't print references with median coverage lower than this")
    parser.add_argument("--min-mean-cov", dest="min_mean", default=0, type=float, help="Don't print references with mean coverage lower than this")
    parser.add_argument("--min-length", dest="min_length", default=0, type=int, help="Don't print references shorter than this")
    parser.add_argument("--min-mapped-ratio", dest="min_mapped", default=0, type=float, help="Don't print references with mapped ratio (bases covered / reference length) less than this")
    parser.add_argument("mpileup")
    parser.add_argument("ref_seqs", help="Reference sequence file")

    args = parser.parse_args()

    refseq_lengths = {}
    for seq in SeqIO.parse(open(args.ref_seqs), "fasta"):
        refseq_lengths[seq.id] = len(seq.seq)

    ref_cov = {}
    all_cov = []
    for line in open(args.mpileup):
        lexemes = line.strip().split("\t")

        if len(lexemes) != 6:
            continue

        refid = lexemes[0]
        cov = int(lexemes[3])

        if refid not in ref_cov:
            ref_cov[refid] = []

        ref_cov[refid].append(cov)
        all_cov.append(cov)

    print "#refid\tmedian_cov\tmean_cov\tcovered_pos\tcovered_ratio"
    for refid in sorted(ref_cov.keys()):
        coverage = ref_cov[refid]
        mapped_length = len(coverage)
        ref_length = refseq_lengths.get(refid)
        uncovered = max(ref_length - mapped_length, 0)
        if uncovered > 0:
            coverage.extend([0] * uncovered)

        median = numpy.median(coverage)
        mean = numpy.mean(coverage)
        mapped_ratio = mapped_length / float(ref_length)

        if median >= args.min_median and mean >= args.min_mean and mapped_ratio >= args.min_mapped and ref_length >= args.min_length:
            print "{0}\t{1}\t{2}\t{3}\t{4}".format(refid, median, mean, mapped_length, mapped_ratio)

if __name__ == "__main__":
    main()
