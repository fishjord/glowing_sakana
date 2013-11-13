#!/usr/bin/env python

import sys

if len(sys.argv) != 3:
	print "USAGE: create_unifrac_sm.py <idmapping> <sample_mapping>"
	sys.exit(1)

sample_mapping = dict()

for line in open(sys.argv[2]):
	lexemes = line.strip().split()
	sample_mapping[lexemes[0]] = lexemes[1]

for line in open(sys.argv[1]):
	lexemes = line.strip().split()
	seqids = lexemes[1].split(",")
	
	print seqids[0], sample_mapping[seqids[0]], len(seqids)
