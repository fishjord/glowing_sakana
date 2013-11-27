#!/usr/bin/python

from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
args = parser.parse_args()

for seq in SeqIO.parse(open(args.input_file), "fasta"):
    desc = seq.description.split()
    id = desc[0]
    if len(desc) > 1:
        desc = " ".join(desc[1:])
    else:
        desc = ""
    
    if ";" in id:
        idx = id.find(";")
        if id[-1] != ";":
            id += ";"
        desc = id[idx:] + desc
        id = id[:idx]
    elif ";" in desc:
        id += desc
        desc = ""

    print ">{0} {1}\n{2}".format(id, desc, seq.seq)
        
