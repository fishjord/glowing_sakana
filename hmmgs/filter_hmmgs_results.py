#!/usr/bin/python

import hmmgs_utils
import argparse
import copy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-length", dest="min_prot_length", default=0, help="Minimum protein length", type=int)
    parser.add_argument("--max-length", dest="max_prot_length", default=10000, help="Maximum protein length", type=int)
    parser.add_argument("--min-bits", dest="min_bits_saved", default=-10000, help="Minimum bits saved", type=float)
    parser.add_argument("--max-bits", dest="max_bits_saved", default=10000, help="Maximum bits saved", type=float)
    parser.add_argument("--min-bits-ratio", dest="min_bits_ratio", default=0, help="Minimum bits saved per position", type=float)
    parser.add_argument("--max-bits-ratio", dest="max_bits_ratio", default=10000, help="Maximum bits saved per position", type=float)
    parser.add_argument("--direction", dest="direction", help="Search direction", default=set(["left", "right"]), type=float, choices=["left", "right"])
    parser.add_argument("hmmgs_file")

    #min_prot_length=0, max_prot_length=10000, min_bits_saved=-1000, max_bits_saved=10000, min_bits_ratio=0, max_bits_ratio=10000, direction=set(["left", "right"]), state_after=0, state_before=10000

    args = parser.parse_args()

    hmmgs_lines = [x for x in hmmgs_utils.read_hmmgs_file(args.hmmgs_file)]
    hmmgs_utils.plot_bits_ratio(hmmgs_lines, "prefilter.png")

    filter_params = copy.copy(vars(args))
    del filter_params["hmmgs_file"]

    filtered_lines = hmmgs_utils.filter(hmmgs_lines, **filter_params)
    hmmgs_utils.plot_bits_ratio(filtered_lines, "postfilter.png")

    for line in filtered_lines:
        print line.contig_id

if __name__ == "__main__":
    main()
