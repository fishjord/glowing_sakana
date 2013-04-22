#!/usr/bin/env python

import sys
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--title", help="Plot title")
parser.add_argument("--plot-ratio", dest="raw", help="Plot raw data", default=True, action="store_false")
parser.add_argument("input_file", help="Input data files")

args = parser.parse_args()

data = {}

xlab = None
ylab = None

y_total = 0
for line in open(args.input_file):
    if line[0] == "#":
        lexemes = line[1:].strip().split()
        
        xlab = lexemes[0]
        ylab = lexemes[1]
    else:
        lexemes = line.strip().split()
        if len(lexemes) > 1:
            x = float(lexemes[0])
            y = float(lexemes[1])

            if x in data:
                raise IOError("Multiple values specified for x value %s" % x)
            data[x] = y
            y_total += y

x = []
y = []
culm = 0

for point in sorted(data.keys()):
    x.append(point)
    culm += data[point]
    if args.raw:
        y.append(culm)
    else:
        y.append(culm / y_total)

plt.plot(x, y)
if args.title:
    plt.title(args.title)
if xlab:
    plt.xlabel(xlab)
    plt.ylabel(ylab)

plt.savefig("%s_accumulation.png" % args.input_file)
