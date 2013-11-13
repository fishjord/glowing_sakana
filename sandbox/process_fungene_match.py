#!/usr/bin/env python

import numpy
import sys
from Bio import SeqIO

if len(sys.argv) != 4:
	print "USAGE: process_fungene_match.py <ref_desc> <fungene_match_file> <max_dissimilarity>"
	sys.exit(1)

ref_hits = dict()
ref_desc = dict()

ref_desc_file = sys.argv[1]
fungene_match_file = sys.argv[2]
max_dissim = float(sys.argv[3])
unclassified = 0

for line in open(ref_desc_file):
	lexemes = line.strip().split("\t")

	if len(lexemes) == 3:
		ref_desc[lexemes[0]] = (lexemes[1], lexemes[2])

for line in open(fungene_match_file):
	lexemes = line.strip().split()
	if len(lexemes) != 3:
		continue

	seqid = lexemes[0]
	refid = lexemes[1]
	dissim = float(lexemes[2])

	if dissim > max_dissim:
		print >>sys.stderr, line.strip()
		unclassified += 1
		continue

	if refid not in ref_hits:
		ref_hits[refid] = []

	ref_hits[refid].append(dissim)

sorted_refids = sorted(ref_hits, key=lambda(x): -len(ref_hits[x]))

print "refid\thits\tavg_dissim\tstd\tdesc\tlinage"
for refid in sorted_refids:
	if refid in ref_desc:
		desc, linage = ref_desc[refid]
	else:
		desc, linage = ("", "")

	dissims = ref_hits[refid]
	print "%s\t%s\t%s\t%s\t%s\t%s" % (refid, len(dissims), numpy.mean(dissims), numpy.std(dissims), desc, linage)
