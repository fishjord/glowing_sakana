#!/usr/bin/env python

import sys
import numpy
from Bio import SeqIO

def read_read_mapping(f):
    read_kmers = dict()

    k = None
    for line in open(f):
        lexemes = line.strip().split()
        if len(lexemes) < 1:
            continue

        kmer = lexemes[0].lower()
        kmer_length = len(kmer)

        if not k:
            k = kmer_length
        elif k != kmer_length:
            raise IOError("Excpected k length %s not %s" % (k, kmer_length))
        read_kmers[kmer] = set(lexemes[1:])

    return k, read_kmers

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: read_counting.py <read_kmer_map> <contig_group>"
        sys.exit(1)

    read_map_file = sys.argv[1]
    contig_file = sys.argv[2]

    k, read_map = read_read_mapping(read_map_file)
    print >>sys.stderr, "Read kmer map, total kmers= %s, k= %s" % (len(read_map), k)

    print "#seqid\tmedian_cov\tmean_cov\tratio_covered"
    print >>sys.stderr, "#seqid\tcoverage"
    for seq in SeqIO.parse(open(contig_file), "fasta"):
        seq_str = str(seq.seq).lower()
        seq_len = len(seq_str)

        contig_kmers = []
        coverage = []

        for i in range(seq_len - k + 1):
            contig_kmers.append(seq_str[i:i+k])

        for seq_index in range(seq_len):
            start = seq_index - 29
            if start < 0:
                start = 0

            contributing_reads = set()
            for k_index in range(start, seq_index + 1):
                if k_index >= len(contig_kmers):
                    break
                if contig_kmers[k_index] in read_map:
                    contributing_reads |= read_map[contig_kmers[k_index]]
                else:
                    print >>sys.stderr, "Kmer %s not in read map" % contig_kmers[k_index]

            coverage.append(len(contributing_reads))

        print "{0}\t{1:}\t{2:.2f}\t{3:.2f}".format(seq.id, numpy.median(coverage), numpy.mean(coverage), (len(coverage) - coverage.count(0)) / float(len(coverage)))
        print >>sys.stderr, "%s\t%s" % (seq.id, " ".join([str(x) for x in coverage]))
