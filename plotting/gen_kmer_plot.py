#!/usr/bin/python

from Bio import SeqIO
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import re

def create_counts(k_file):
    kmer_counts = {}
    for line in open(k_file):
        if line.strip() == "":
            continue

        lexemes = line.strip().split()

        if len(lexemes) == 1:
            cnt = 0
        else:
            cnt = len(lexemes[1:])

        kmer_counts[lexemes[0]] = cnt

    return kmer_counts

def get_kmers(seq, k):
    kmers = []
    seq_str = str(seq.seq).lower()
    for i in range(len(seq_str) - k + 1):
        kmers.append(seq_str[i:i+k])

    return kmers

def histo(kmers, cnts):
    ret = {}
    for kmer in kmers:
        cnt = cnts.get(kmer, 0)
        ret[cnt] = ret.get(cnt, 0) + 1

    x, y = [], []

    for i in sorted(ret.keys()):
        x.append(i)
        y.append(ret[i])

    return x, y

if len(sys.argv) < 3:
    print "USAGE: gen_plot.py <ref_file> <k_files>"
    sys.exit(1)

seqs = [x for x in SeqIO.parse(open(sys.argv[1]), "fasta")]

n = int(math.ceil(math.sqrt(len(seqs))))
regex = re.compile(".+k(\d+).+")

for k_file in sys.argv[2:]:
    kmer_counts = create_counts(k_file)
    m = regex.match(k_file)
    if not m:
        raise Exception("Couldn't find k-value in file name '%s'" % k_file)

    k = int(m.groups()[0])

    fig = plt.figure()
    fig.set_figheight(20)
    fig.set_figwidth(25)
    #fig.set_title("k%s" % k)

    for i in range(len(seqs)):
        ax = fig.add_subplot(n, n, i)
        x, y = histo(get_kmers(seqs[i], k), kmer_counts)

        ax.bar(x, y)
        ax.set_xlabel("Occurance")
        ax.set_ylabel("Count")
        ax.set_title("%s" % (" ".join(seqs[i].description.split()[1:])))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 900)

    #plt.tight_layout()
    plt.savefig("%s_abund.png" % k_file)
    plt.clf()
