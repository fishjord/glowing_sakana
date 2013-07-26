#!/usr/bin/env python

import sys
import argparse
import matplotlib

matplotlib.use('agg')

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--title", help="Plot title")
parser.add_argument("--plot-ratio", dest="raw", help="Plot raw data", default=True, action="store_false")
parser.add_argument("--reverse", dest="reverse", default=False, action="store_true")
parser.add_argument("input_file", help="Input data files")

args = parser.parse_args()

data = {}

xlab = None
if args.raw:
    ylab = "Count"
else:
    ylab = "Ratio"

total = 0
for line in open(args.input_file):
    if line[0] == "#":
        lexemes = line[1:].strip().split()
        
        xlab = lexemes[0]
    else:
        lexemes = line.strip().split()
        if len(lexemes) == 1:
            x = float(lexemes[0])

            data[x] = data.get(x, 0) + 1
            total += 1

x = []
y = []
culm = 0

for point in sorted(data.keys(), reverse=args.reverse):
    x.append(point)
    culm += data[point]
    if args.raw:
        y.append(culm)
    else:
        y.append(culm / total)

plt.plot(x, y)
if args.title:
    plt.title(args.title)
if xlab:
    plt.xlabel(xlab)
plt.ylabel(ylab)

plt.savefig("%s_accumulation.png" % args.input_file)
