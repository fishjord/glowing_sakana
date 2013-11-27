#!/usr/bin/env python

import sys

input_files = []
line = None
for f in sys.argv[1:]:
    input_files.append(open(f))
    line = input_files[-1].readline()
    if line[0] != "#":
        raise IOError("Missing header in {0}".format(f))

print line

while True:
    #rank   taxid   name    parent  total_seqs      intra_sum       intra_edges     inter_sum       inter_edges     nan edges
    #rootrank        0       Root    -1      2658609 49322133641622  25114989073     0       0       602686113
    out = None
    for f in input_files:
        line = f.readline()
        if line == "":
            if out == None:
                break
            else:
                raise IOError("One file ended before the others")

        line = line.split("\t")
        if len(line) != 10:
            raise IOError("Invalid line {0}".format(line))

        for i in range(5, 10):
            line[i] = int(line[i])

        if out == None:
            out = line
        else:
            for i in range(5, 10):
                out[i] += line[i]

    if out == None:
        break
    print "\t".join(["{0}".format(x) for x in out])
