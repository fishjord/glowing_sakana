#!/usr/bin/env python

import os
import sys

if len(sys.argv) != 4:
	print "USAGE: filter_hmmgs.py <output> <column> <min_bits>"
	sys.exit(1)

tab_file = sys.argv[1]
column = int(sys.argv[2])
min_value = float(sys.argv[3])

passed = open("passed_" + os.path.split(tab_file)[1], "w")
failed = open("failed_" + os.path.split(tab_file)[1], "w")

for line in open(tab_file):
	lexemes = line.strip().split("\t")

	if line[0] == "#" or len(lexemes) <= column:
		continue

	if lexemes[column] == "-":
		value = -10000
	else:
		value = float(lexemes[column])

	if value < min_value:
		failed.write(line)
	else:
		passed.write(line)
