#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: convert_mothur_rdp_clust.py <mothur_list_file>"

tot_seqs = 0

for line in open(sys.argv[1]):
    lexemes = line.strip().split()
    for clust in lexemes[2:]:
        tot_seqs += len(clust.split(","))

out = open("%s.clust" % sys.argv[1], "w")

out.write("File(s):\t%s\n" % sys.argv[1])
out.write("Sequences:\t%s\n" % tot_seqs)

for line in open(sys.argv[1]):
    lexemes = line.strip().split()

    cutoff = lexemes[0]
    tot_clusts = lexemes[1]
    clusters = lexemes[2:]
    
    out.write("\ndistance cutoff:\t%s\n" % cutoff)
    out.write("Total Clusters: %s\n" % tot_clusts)
    cid = 0
    
    for clust in clusters:
        seqs = clust.split(",")
        out.write("%s\t%s\t%s\t%s\n" % (cid, sys.argv[1], len(seqs), " ".join(seqs)))
        cid += 1

out.close()
