#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print >>sys.stderr, "USAGE: plot_two_column_bar.py <input_file> [bins] [title]"
    sys.exit(1)

x = []
y = []

ylab = None

for line in open(sys.argv[1]):
    if line[0] == "#":
        lexemes = line[1:].strip().split("\t")
        ylab = lexemes[0]
    else:
        lexemes = line.strip().split()
        if len(lexemes) == 1:
            y.append(float(lexemes[0]))

if len(sys.argv) > 2:
    num_bins = int(sys.argv[2])
else:
    num_bins = max(y)

print "Bins: %d" % num_bins
plt.hist(y, num_bins)
if len(sys.argv) > 3:
    plt.title(sys.argv[3])

if ylab:
    plt.xlabel(ylab)
    plt.ylabel("count")

plt.savefig("%s_histo.png" % sys.argv[1])
