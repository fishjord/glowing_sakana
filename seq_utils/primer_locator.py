#!/usr/bin/env python

import sys
from Bio import SeqIO

if len(sys.argv) != 5:
    print >>sys.stderr, "USAGE: primer_locator.py <seqfile> <seqid> <seq_pos> <primer>"
    sys.exit(1)

seqid = sys.argv[2]
primer = sys.argv[4]
target_pos = int(sys.argv[3]) - len(primer)

target_seq = None
for seq in SeqIO.parse(open(sys.argv[1]), "fasta"):
    if seq.id == seqid:
        target_seq = seq
        break

if target_seq == None:
    raise Exception("Target seq not found")

seq_str = str(target_seq.seq)
seq_pos = 0
model_pos = 0
msa_pos = 0

print seq_str
for b in seq_str:
    msa_pos += 1
    if b in "acgt":
        seq_pos += 1
    elif b in "ACGT":
        seq_pos += 1
        model_pos += 1
    elif b == "-":
        model_pos += 1
    elif b == ".":
        continue

    if seq_pos == target_pos:
        print "{0}{1}".format("".join([" "] * msa_pos), primer)
        print "Sequence position: {0}".format(seq_pos)
        print "MSA position: {0}".format(msa_pos)
        print "Model position: {0}".format(model_pos)
        break
