#!/usr/bin/python

"""
#gene name      query id        refid   nucl kmer       is prot?        starting_frame  prot kmer       model pos
rplb_prot       SRR172902.46    NP_294037.1     gttcacgcgctcgaactggtt   true    1       vhalelv 142
rplb_prot       SRR172902.46    NP_294037.1     cacgcgctcgaactggttccc   true    1       halelvp 143
rplb_prot       SRR172902.46    NP_294037.1     gcgctcgaactggttcccggc   true    1       alelvpg 144
"""

import hmmgs_utils
import argparse
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--random-seed", dest="seed", type=int, help="Set the random seed", default=0)
    parser.add_argument("-m", "--min-kmer-hits", dest="min_hits", type=int, help="Minimum number of kmer hits a read must produce for the read to pass filtering", default=3)
    parser.add_argument("starts_file")

    args = parser.parse_args()

    random.seed(args.seed)

    seen_starts = set()
    last_qid = ""
    current_hit_list = {}
    for line in hmmgs_utils.read_kmer_starts(args.starts_file):
        if line.query_id == last_qid:
            if line.starting_frame not in current_hit_list:
                current_hit_list[line.starting_frame] = []
            
            current_hit_list[line.starting_frame].append(line)
        else:
            best_frame = None
            for frame in current_hit_list:
                if best_frame == None or len(current_hit_list[best_frame]) < len(current_hit_list[frame]):
                    best_frame = frame

            if len(current_hit_list) > 1:
                print >>sys.stderr, "Query %s had hits in multiple frames: %s" % (last_qid, " ".join("%s= %s" % (x, len(current_hit_list[x])) for x in sorted(current_hit_list.keys())))

            hits = current_hit_list[best_frame]

        

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: random_select.py <kmer starts file>"
    sys.exit(1)


for line in open(sys.argv[1]):
    
