#!/usr/bin/python

import sys

if len(sys.argv) != 3:
    print "USAGE: top_n_blast_hits.py <n> <blast_file>"
    sys.exit(1)

n = int(sys.argv[1])

seqids = dict()
for line in open(sys.argv[2]):
    line = line.strip()
    seqid = line.split("\t")[0]

    cnt = seqids.get(seqid, 0)

    if cnt >= n:
        continue
    
    seqids[seqid] = cnt + 1
    print line
