#!/usr/bin/env python

import numpy
import math
import sys
from Bio import SeqIO

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: msa_entropy.py <sto> [log base=2]"
    sys.exit(1)

def entropy(probs, base=2):
    ent = 0
    for residue in probs:
        p = probs[residue]
        ent += p * math.log(p, base)

    return -ent

base = 2
if len(sys.argv) == 3:
    base = int(sys.argv[2])

column_counts = None
num_seqs = 0
out_ids = set()

for seq in SeqIO.parse(open(sys.argv[1]), "stockholm"):
    print >>sys.stderr, seq.id
    if len(out_ids) == 0:
        for i in range(len(seq.seq)):
            if not(seq.seq[i] == "." or seq.seq[i].lower() == seq.seq[i]):
                out_ids.add(i)            

    if column_counts == None:
        column_counts = [{} for x in seq.seq]

    for i in range(len(seq.seq)):
        residue = str(seq.seq[i]).lower()
        if residue not in ["a", "c", "g", "u"]:
            continue
        
        if residue == "-" or residue == ".":
            continue
        column_counts[i][residue] = column_counts[i].get(residue, 0) + 1
        column_counts[i]["sum"] = column_counts[i].get("sum", 0) + 1.0

    num_seqs += 1

print "Number of seqs: %s" % num_seqs
print "Number of columns: %s" % len(column_counts)

column_probs = []
for i in range(len(column_counts)):
    column_probs.append({})
    if len(column_counts[i]) == 0:
        continue

    for residue in column_counts[i]:
        if residue == "sum":
            continue

        column_probs[i][residue] = column_counts[i][residue] / column_counts[i]["sum"]

print "Column\tcount\tentropy"
column_entropy = []
for i in range(len(column_probs)):
    if out_ids and i not in out_ids:
        continue

    if len(column_counts[i]) == 0:
        print "%s\t-\t-" % (i + 1)
    else:
        column_entropy.append(entropy(column_probs[i], base))
        print "%s\t%s\t%s" % (i + 1, column_counts[i]["sum"], column_entropy[-1])

print "Min entropy: %0.2f, max entropy: %02.f, mean entropy: %0.2f, stdev: %0.2f" % (min(column_entropy), max(column_entropy),  numpy.mean(column_entropy), numpy.std(column_entropy))
