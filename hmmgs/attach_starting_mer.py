#!/usr/bin/python

import sys
import hmmgs_utils
from Bio import SeqIO

if len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: attach_starting_mer.py <hmmgs_file"
    sys.exit(1)

hmmgs_results = {}
for line in hmmgs_utils.read_hmmgs_file(sys.argv[1]):
    hmmgs_results[line[0]] = line


for seq in SeqIO.parse(open(sys.argv[2]), "fasta"):
    pass
