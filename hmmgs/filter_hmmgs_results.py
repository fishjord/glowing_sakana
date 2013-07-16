#!/usr/bin/env python

import hmmgs_utils
import argparse
import copy
from Bio import SeqIO

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-length", dest="min_prot_length", default=0, help="Minimum protein length", type=int)
    parser.add_argument("--max-length", dest="max_prot_length", default=10000, help="Maximum protein length", type=int)
    parser.add_argument("--min-bits", dest="min_bits_saved", default=-10000, help="Minimum bits saved", type=float)
    parser.add_argument("--max-bits", dest="max_bits_saved", default=10000, help="Maximum bits saved", type=float)
    parser.add_argument("--min-bits-ratio", dest="min_bits_ratio", default=0, help="Minimum bits saved per position", type=float)
    parser.add_argument("--max-bits-ratio", dest="max_bits_ratio", default=10000, help="Maximum bits saved per position", type=float)
    parser.add_argument("--stem", dest="stem", default="filtered", help="Output file stem")
    parser.add_argument("--direction", dest="direction", help="Search direction", default=set(["left", "right"]), type=float, choices=["left", "right"])
    parser.add_argument("hmmgs_file")
    parser.add_argument("hmmgs_nucl_seqs")
    parser.add_argument("hmmgs_prot_seqs")

    #min_prot_length=0, max_prot_length=10000, min_bits_saved=-1000, max_bits_saved=10000, min_bits_ratio=0, max_bits_ratio=10000, direction=set(["left", "right"]), state_after=0, state_before=10000

    args = parser.parse_args()

    nucl_seqs = SeqIO.to_dict(SeqIO.parse(open(args.hmmgs_nucl_seqs), "fasta"))
    prot_seqs = SeqIO.to_dict(SeqIO.parse(open(args.hmmgs_prot_seqs), "fasta"))

    hmmgs_lines = [x for x in hmmgs_utils.read_hmmgs_file(args.hmmgs_file)]
    hmmgs_utils.plot_bits_ratio(hmmgs_lines, "prefilter.eps")

    filter_params = copy.copy(vars(args))
    del filter_params["hmmgs_file"]
    del filter_params["stem"]
    del filter_params["hmmgs_nucl_seqs"]
    del filter_params["hmmgs_prot_seqs"]

    filtered_lines = [x for x in hmmgs_utils.filter(hmmgs_lines, **filter_params)]
    hmmgs_utils.plot_bits_ratio(filtered_lines, "postfilter.eps")

    filtered_hmmgs = open("{0}_hmmgs.txt".format(args.stem), "w")
    filtered_nucl = open("{0}_nucl.fasta".format(args.stem), "w")
    filtered_prot = open("{0}_prot.fasta".format(args.stem), "w")

    hmmgs_header = hmmgs_utils.read_hmmgs_header(args.hmmgs_file)
    hmmgs_utils.write_hmmgs_header(filtered_hmmgs, hmmgs_header)
    for line in filtered_lines:
        hmmgs_utils.write_hmmgs_line(filtered_hmmgs, hmmgs_header, line)
        filtered_nucl.write(">{0}\n{1}\n".format(line["contig_id"], nucl_seqs[line["contig_id"]].seq))
        filtered_prot.write(">{0}\n{1}\n".format(line["contig_id"], prot_seqs[line["contig_id"]].seq))

if __name__ == "__main__":
    main()
