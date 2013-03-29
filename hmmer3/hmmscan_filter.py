#!/usr/bin/python

import os
import sys

if len(sys.argv) < 2:
	print >>sys.stderr,  "USAGE: hmmscan_filter.py [-b <min_bits>] [-dl <min_dom_length>] [-e max_eval] <hmm_scan_files>..."
	sys.exit(1)

min_bits = -1000
min_length = 0
max_eval = 10

i = 1
hmm_scan_files = []
while i < len(sys.argv):
	if sys.argv[i] == "-b":
		i += 1
		min_bits = float(sys.argv[i])
	elif sys.argv[i] == "-dl":
		i += 1
		min_length = int(sys.argv[i])
	elif sys.argv[i] == "-e":
		i += 1
		max_eval = float(sys.argv[i])
	else:
		hmm_scan_files.append(sys.argv[i])

	i += 1

inlines = 0
outlines = 0
for f in hmm_scan_files:
	out_file = os.path.split(f)[1]
	out = open("min_%s_%s" % (min_bits, out_file), "w")
	for line in open(f):
		inlines += 1
		if line[0] == "#":
			out.write(line)
			continue

		lexemes = line.strip().split()
		if len(lexemes) == 23:
			bits = float(lexemes[7])
			eval = float(lexemes[6])
			length = int(lexemes[18]) - int(lexemes[17])
		elif len(lexemes) == 19:
			bits = float(lexemes[5])
			length = 5000 #don't get a length from a global scan...so kludge ahoy
			eval = float(lexemes[4])
		else:
			continue

		if bits >= min_bits and length >= min_length and eval <= max_eval:
			outlines += 1
			out.write(line)

	out.close()

print >>sys.stderr, "Scanned %s hmmscan files for a total of %s lines read, %s lines written with minbits %s, min length %s and max eval %s" % (len(hmm_scan_files), inlines, outlines, min_bits, min_length, max_eval)
