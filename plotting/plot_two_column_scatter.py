#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print >>sys.stderr, "USAGE: plot_two_column_scatter.py <input_file> [title]"
    sys.exit(1)

x = []
y = []

xlab = None
ylab = None

for line in open(sys.argv[1]):
    if line[0] == "#":
        lexemes = line[1:].strip().split()
        xlab = lexemes[0]
        ylab = lexemes[1]
    else:
        lexemes = line.strip().split()
        if len(lexemes) > 1:
            x.append(float(lexemes[0]))
            y.append(float(lexemes[1]))

plt.scatter(x, y)
if len(sys.argv) > 3:
    plt.title(sys.argv[2])
if xlab:
    plt.xlabel(xlab)
    plt.ylabel(ylab)

plt.savefig("%s_scatter_plot.png" % sys.argv[1])
