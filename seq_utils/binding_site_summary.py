#!/usr/bin/env python

import sys
import string
from Bio import SeqIO

if len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: binding_site_summary.py <binding_sites.txt> <seqfile>"
    sys.exit(1)

seqfile = sys.argv[2]
binding_sites = {}

for line in open(sys.argv[1]):
    if line[0] == "#":
        continue

    lexemes = line.strip().split("\t")
    if len(lexemes) != 5:
        print lexemes
        continue

    refseq = lexemes[0]
    desc = lexemes[1]
    pos = int(lexemes[2])
    model_pos = int(lexemes[3]) + 1
    expected_aa = lexemes[4]

    if model_pos in binding_sites:
        raise Exception("Multiple binding sites for model position {0}\nOffending line: {1}".format(model_pos, line.strip()))
    binding_sites[model_pos] = expected_aa            

for seq in SeqIO.parse(open(seqfile), "fasta"):
    if seq.id[0] == "#":
        continue

    seq_str = str(seq.seq)
    seq_pos = 0
    model_pos = 0
    msa_pos = 0

    covered_sites = []
    aas = []
    matching = 0

    for b in seq_str:
        msa_pos += 1
        if b in string.ascii_lowercase:
            seq_pos += 1
        elif b in string.ascii_uppercase:
            seq_pos += 1
            model_pos += 1

            if model_pos in binding_sites:
                covered_sites.append(model_pos)
                aas.append(b)
                if b == "L" and model_pos == 186:
                    print >>sys.stderr, ">{0}\n{1}".format(seq.id, seq.seq)

                if b == binding_sites[model_pos]:
                    matching += 1
        elif b == "-":
            model_pos += 1
        elif b == ".":
            continue

    if len(covered_sites) > 0:
        ratio_matching = float(matching) / len(covered_sites)
    else:
        ratio_matching = float("NaN")

    print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(seq.id, ",".join([str(x) for x in covered_sites]), ",".join(aas), len(covered_sites), matching, ratio_matching)
