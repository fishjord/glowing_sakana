#!/usr/bin/python

import hmmgs_utils
import sys


if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: extract_top_hits.py <hmmgs_file>"
    sys.exit(1)

last_dir = "right"
last_score = 0

for line in hmmgs_utils.read_hmmgs_file(sys.argv[1]):
    if line.search_direction != last_dir or line.nats == last_score:
        print line.line
        last_dir = line.search_direction
        last_score = line.nats
