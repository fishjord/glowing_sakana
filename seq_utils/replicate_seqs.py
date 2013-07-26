#!/usr/bin/env python

import sys
import argparse
from Bio import SeqIO


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--default-count", default=0, dest="default_count", type=int, help="For sequences without coverage information, assume this coverage")
    parser.add_argument("seqfile")
    parser.add_argument("counts_file")

    args = parser.parse_args()

    seq_counts = {}
    for line in open(args.counts_file):
        if line[0] == "#":
            continue
        lexemes = line.strip().split("\t")
        if len(lexemes) > 2:
            seqid = lexemes[0]
            cnt = int(float(lexemes[1]) + .5)

            seq_counts[seqid] = cnt

    for seq in SeqIO.parse(open(args.seqfile), "fasta"):
        cnt = seq_counts.get(seq.id, args.default_count)
        if cnt == 0:
            print >>sys.stderr, "{0}\tZero count".format(seq.id)

        for i in range(cnt):
            print ">{0}_{1}\n{2}".format(seq.id, i + 1, seq.seq)
        
if __name__ == "__main__":
    main()
    



    
