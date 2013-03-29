#!/usr/bin/python

import sys
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import re
import numpy
import locale

def pretty_print(num_bytes):
    """
    Output number of bases, modified from url size computation located at http://homepages.inf.ed.ac.uk/imurray2/code/hacks/urlsize
    """
    KiB = 1000.0
    MiB = KiB * KiB
    GiB = KiB * MiB
    TiB = KiB * GiB
    PiB = KiB * TiB
    EiB = KiB * PiB
    ZiB = KiB * EiB
    YiB = KiB * ZiB

    output = "%s B" % num_bytes
    if num_bytes > YiB:
        output = '%.3g YB' % (num_bytes / YiB)
    elif num_bytes > ZiB:
        output = '%.3g ZB' % (num_bytes / ZiB)
    elif num_bytes > EiB:
        output = '%.3g EB' % (num_bytes / EiB)
    elif num_bytes > PiB:
        output = '%.3g PB' % (num_bytes / PiB)
    elif num_bytes > TiB:
        output = '%.3g TB' % (num_bytes / TiB)
    elif num_bytes > GiB:
        output = '%.3g GB' % (num_bytes / GiB)
    elif num_bytes > MiB:
        output = '%.3g MB' % (num_bytes / MiB)
    elif num_bytes > KiB:
        output = '%.3g KB' % (num_bytes / KiB)

    return output

def read_name_mapping(fname):
    name_mapping = {}
    region_mapping = {}
    for line in open(fname):
        lexemes = line.strip().split("\t")
        if len(lexemes) > 1:
            name_mapping[lexemes[0]] = lexemes[1]
        if len(lexemes) > 3:
            region_mapping[lexemes[0]] = (int(lexemes[2]), int(lexemes[3]))

    return name_mapping, region_mapping

def smooth(coverage):
    ret = []
    window = max(1, int(len(coverage) * .001))
    x = []
    if window == 1:
        return coverage, range(1, len(coverage) + 1)

    for i in range(0, len(coverage), window):
        ret.append(sum(coverage[i:i+window]) / window)
        x.append(i + 1)

    return ret, x

def plot_coverage(seqid, name, coverage, matches, mismatches):
    if seqid == name:
        print_name = "(none)"
    else:
        print_name = name
    
    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (seqid, name, pretty_print(len(coverage)), min(coverage), max(coverage), numpy.average(coverage), numpy.median(coverage), numpy.std(coverage), numpy.mean(mismatches), numpy.median(mismatches), numpy.std(mismatches))

    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(30)

    ax = fig.add_subplot(1,1,1)

    ax.set_title(name)

    y, x = smooth(matches)
    ax.plot(x, y, "b-")

    y, x = smooth(coverage)
    ax.plot(x, y, "r-")

    ax.set_xlabel("Position in reference")
    ax.set_ylabel("Coverage")
    ax.set_xlim(1, x[-1])
    ax.set_ylim(0, max(y) + 5)

    ax.legend(["coverage", "exact ref match"], loc=1)

    plt.savefig("%s_coverage.png" % seqid)
    plt.clf()

def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print >>sys.stderr, "USAGE: gen_plot.py <mpileup.txt> [ids to names]"
        sys.exit(1)

    if len(sys.argv) == 3:
        name_mapping, region_mapping = read_name_mapping(sys.argv[2])
    else:
        name_mapping = {}
        region_mapping = {}

    last_seqid = None
    cov_list = []
    cov_exact = []
    curr_region = (0, 100000000000)
    mismatches = []
    skipped = set()

    print "#seqid\tname\tlength\tmin_cov\tmax_cov\tavg_cov\tmedian_cov\tcov_sd\tavg_errors\tmedian_errors\terror_sd"
    for line in open(sys.argv[1]):
        lexemes = line.strip().split()
        if len(lexemes) != 6:
            continue

        #gi|126640115|ref|NC_009085.1|   17      N       6       AAAAAA  AAABAB
        seqid = lexemes[0]
        #if "|" in seqid:
        #    seqid = seqid.split("|")[-2]

        if seqid != last_seqid:
            if len(cov_list) > 0:
                plot_coverage(last_seqid, name_mapping.get(last_seqid, last_seqid), cov_list, cov_exact, mismatches)
            cov_list = []
            cov_exact = []
            mismatches = []
            last_seqid = seqid
            curr_region = region_mapping.get(seqid, (-1, 100000000000))

        if len(name_mapping) > 0 and seqid not in name_mapping:
            if seqid not in skipped:
                skipped.add(seqid)
            continue

        pos = int(lexemes[1])

        if pos < curr_region[0] or pos > curr_region[1]:
            continue

        ref_base = lexemes[2]
        cov = int(lexemes[3])
        bases = lexemes[4]
        qual_scores = lexemes[5]

        matches = 0
        if ref_base != "N":
            for i in range(len(bases)):
                if (bases[i] == "," or bases[i] == ".") and bases[i - 1] != '^':
                    matches += 1

        if matches > cov:
            raise IOError(line.strip())

        while pos - curr_region[0] > len(cov_list):
            cov_list.append(0)
            cov_exact.append(0)
            mismatches.append(0)
        
        cov_list.append(cov)
        cov_exact.append(matches)
        mismatches.append(cov - matches)

    if len(cov_list) > 0:
        plot_coverage(last_seqid, name_mapping.get(last_seqid, last_seqid), cov_list, cov_exact, mismatches)


if __name__ == "__main__":
    main()

