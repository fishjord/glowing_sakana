#!/usr/bin/python

import sys
import hmmgs_utils
import argparse

def filter_and_write(current_hit_list, last_qid, seen_starts, min_hits):
    if len(current_hit_list) == 0:
        return

    best_frame = None
    for frame in current_hit_list:
        if best_frame == None or len(current_hit_list[best_frame]) < len(current_hit_list[frame]):
            best_frame = frame

    if len(current_hit_list) > 1:
        print >>sys.stderr, "Query %s had hits in multiple frames: %s" % (last_qid, " ".join("%s= %s" % (x, len(current_hit_list[x])) for x in sorted(current_hit_list.keys())))

    hits = current_hit_list[best_frame]

    if len(hits) > min_hits:
        for line in hits:
            id = "%s%s" % (line.nucl_kmer,line.model_pos)
            if id not in seen_starts:
                seen_starts.add(id)
                print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (line.gene_name, line.query_id, line.refid, line.nucl_kmer, line.is_prot, line.starting_frame, line.prot_kmer, line.model_pos)            

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--min-kmer-hits", dest="min_hits", type=int, help="Minimum number of kmer hits a read must produce for the read to pass filtering", default=3)
    parser.add_argument("starts_file")

    args = parser.parse_args()

    seen_starts = set()
    last_qid = ""
    current_hit_list = {}
    in_starts = 0
    queries = 0
    for line in hmmgs_utils.read_kmer_starts(args.starts_file):
        in_starts += 1
        if line.query_id == last_qid:
            if line.starting_frame not in current_hit_list:
                current_hit_list[line.starting_frame] = []
            
            current_hit_list[line.starting_frame].append(line)
        else:
            filter_and_write(current_hit_list, last_qid, seen_starts, args.min_hits)
            last_qid = line.query_id
            queries += 1
            current_hit_list = {}

    filter_and_write(current_hit_list, last_qid, seen_starts, args.min_hits)

    print >>sys.stderr, "Read in %s starting nodes from %s queries in %s and wrote out %s (min_hits= %s)" % (in_starts, queries, args.starts_file, len(seen_starts), args.min_hits)

if __name__ == "__main__":
    main()
