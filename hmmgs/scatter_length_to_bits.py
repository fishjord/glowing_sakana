#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import hmmgs_utils
import sys

if len(sys.argv) != 3:
    print "USAGE: scatter_length_to_bits.py <hmmgs_file> <chart_file>"
    sys.exit(1)

lengths = []
bits = []

for line in hmmgs_utils.read_hmmgs_file(sys.argv[1]):
    prot_length = int(line.prot_length)
    bits_saved = float(line.bits)

    lengths.append(prot_length)
    bits.append(bits)

plt.scatter(lengths, bits)
plt.savefig(sys.argv[2])
