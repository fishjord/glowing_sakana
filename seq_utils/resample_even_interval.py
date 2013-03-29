#!/usr/bin/python

import sys

if len(sys.argv) != 3:
	print "USAGE: resample_even_interval.py <infile> <# samples>"
	sys.exit(1)

infile = sys.argv[1]
num_samples = int(sys.argv[2])

lines = list(open(infile))
interval = len(lines) / num_samples

for i in range(0, len(lines), interval):
	print lines[i].strip()
