#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from collections import namedtuple

class hmmgs_line:
    pass

def plot_bits_ratio(hmmgs_lines, fname = None):
    lengths = [x.prot_length for x in hmmgs_lines]
    bits = [x.bits for x in hmmgs_lines]
    bits_ratios = [x.bits_ratio for x in hmmgs_lines]

    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.scatter(lengths, bits)
    ax.set_xlabel("prot length")
    ax.set_ylabel("bits saved")
    ax.set_title("Length vs Bits Saved")

    ax2 = fig.add_subplot(122)
    n, bins, patches = ax2.hist(sorted(bits_ratios), 100, facecolor='green', alpha=.75, histtype='step')
    bincenters = 0.5 * (bins[1:] + bins[:-1])
    y = mlab.normpdf(bincenters, 100, 15)
    l = ax2.plot(bincenters, y, 'r--', linewidth=1)

    ax2.set_xlabel("bits ratio")
    ax2.set_ylabel("count")
    ax2.set_title("Histogram of bits saved to length")

    if fname != None:
        plt.savefig(fname)

def read_kmer_starts(fname):
    stream = open(fname)
    header = stream.readline().strip()
    if header[0] != '#':
        raise IOError("Malformed header line in file %s: '%s'" % (fname, header))
    header = header[1:].replace(" (s)", "").replace("?", "").replace(" ", "_").split("\t")

    for line in stream:
        lexemes = line.strip().split()
        if len(lexemes) != len(header):
            continue

        ret = hmmgs_line()
        for i in range(len(header)):
            try:
                val = int(lexemes[i])
            except:
                try:
                    val = float(lexemes[i])
                except:
                    val = lexemes[i]

            vars(ret)[header[i]] = val

        yield ret

def read_hmmgs_file(fname):
    stream = open(fname)
    header = stream.readline().strip()
    if header[0] != '#':
        raise IOError("Malformed header line in file %s: '%s'" % (fname, header))
    header = header[1:].replace(" (s)", "").replace(" ", "_").split("\t")
    
    for line in stream:
        lexemes = line.strip().split()
        if len(lexemes) != len(header):
            continue

        ret = hmmgs_line()
        for i in range(len(header)):
            try:
                val = int(lexemes[i])
            except:
                try:
                    val = float(lexemes[i])
                except:
                    val = lexemes[i]

            vars(ret)[header[i]] = val

        ret.bits_ratio = ret.bits / ret.prot_length
        ret.line = line.strip()

        yield ret

def filter(hmmgs_lines, min_prot_length=0, max_prot_length=10000, min_bits_saved=-1000, max_bits_saved=10000, min_bits_ratio=0, max_bits_ratio=10000, direction=set(["left", "right"]), state_after=0, state_before=10000):
    ret = []
    for l in hmmgs_lines:
        if l.prot_length < min_prot_length or l.prot_length > max_prot_length:
            continue

        if l.bits < min_bits_saved or l.bits > max_bits_saved:
            continue

        if l.search_direction not in direction:
            continue

        if l.starting_state < state_after or l.starting_state > state_before:
            continue

        if l.bits_ratio < min_bits_ratio or l.bits_ratio > max_bits_ratio:
            continue

        ret.append(l)

    return ret
