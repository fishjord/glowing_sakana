#!/usr/bin/python

import os
import sys
import argparse
import math

"""
ex. format

#comment

  A   C  G  T
A  5 -1 -1 -1
C -1  5 -1 -1
G -1 -1  5 -1
T -1 -1 -1  5

"""
def parse_sm(sm_file):
    ret = []
    header_parsed = False
    for line in open(sm_file):
        if line[0] == "#":
            continue

        line = line.strip()
        if line == "":
            continue

        if not header_parsed:
            header_parsed = True
            continue

        ret.append([float(x) for x in line.split()[1:]])

    return ret

def test_sm(sm):
    avg = 0
    tot = 0
    one_gt_0 = False

    for row in sm:
        for val in row:
            avg += val
            tot += 1

            if val > 0:
                one_gt_0 = True

    avg /= tot

    return avg < 0 and one_gt_0

def calc_tot_prob(sm, priors, l):
    tot = 0
    for a in range(len(sm)):
        for b in range(len(sm)):
           tot += priors[a] * priors[b] * math.exp(l * sm[a][b]) 
    return tot

def recover_l(sm, priors):
    guess = 0.1
    lower = 0
    upper = guess

    while True:
        upper *= 2
        if calc_tot_prob(sm, priors, upper) >= 1:
            break
        else:
            lower = upper

    while True:
        guess = .5 * (lower + upper)

        if(calc_tot_prob(sm, priors, guess) > 1):
            upper = guess
        else:
            lower = guess

        if abs(upper - lower) < 1E-7:
            break

    return 1 / (.5 * (upper + lower))

def recover_prob(sm, priors, l):
    ret = [None] * len(sm)

    for a in range(len(sm)):
        new_row = [None] * len(sm[a])

        for b in range(len(sm[a])):
            new_row[b] = priors[a] * priors[b] * math.exp((float(1) / l) * sm[a][b])

        ret[a] = new_row

    return ret

def information(prob_matrix, priors):
    h = 0

    for a in range(len(prob_matrix)):
        for b in range(len(prob_matrix)):
            h += prob_matrix[a][b] * math.log(prob_matrix[a][b] / (priors[a] * priors[b]), 2)

    return h

def calc_expected(K, m, query_size, lam, score):
    return K * m * query_size * math.exp(-(1/float(lam)) * score)

def find_db_size(K, lam, query_size, score, max_expected):
    return max_expected / (K * query_size * math.exp(-(1/float(lam)) * score))
    guess = 0.1
    lower = 0
    upper = guess

    while True:
        upper *= 100
        if calc_expected(K, upper, query_size, lam, score) >= max_expected:
            break
        else:
            lower = upper

    while True:
        guess = .5 * (lower + upper)

        if calc_expected(K, guess, query_size, lam, score) > max_expected:
            upper = guess
        else:
            lower = guess

        if abs(upper - lower) < 1E-7:
            break

    return 1 / (.5 * (upper + lower))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--priors", help="Specific residue priors (1 per letter, seperated by ',', ie .25,.25,.25,.25), default=uniform prior", dest="priors")
    parser.add_argument("scoring_matrix")

    args = parser.parse_args()

    sm = parse_sm(args.scoring_matrix)

    if args.priors:
        priors = [float(x) for x in args.priors.split(",")]
    else:
        priors = [1 / float(len(sm)) for x in range(len(sm))]

    if abs(1 - sum(priors)) > .0001:
        print >>sys.stderr, "Sum of priors is not 1!"
        sys.exit(1)

    if len(priors) != len(sm):
        print >>sys.stderr, "Number of priors (%s) not equal to number of residues (%s)" % (len(priors), len(sm))
        sys.exit(1)

    l = recover_l(sm, priors)
    prob_matrix = recover_prob(sm, priors, l)
    h = information(prob_matrix, priors)

    pretty_name = os.path.split(args.scoring_matrix)[-1]
    print "%s lambda=%.02f" % (pretty_name, l)
    print "%s target probabilities:\n%s" % (pretty_name, "\n".join([" ".join([str(y) for y in x]) for x in prob_matrix]))
    print "%s bits/base information: %.02f" % (pretty_name, h)

    sys.exit(0)
    print
    print "Thresholds"
    print "length\ts35\thoxd70\ts35_max_dbsize_e-5\ts_35_max_db_size_e-10"
    for l in lengths:
        s35_score = s35_h * s35_l * l
        
        s35_dbsize_maxsize_e5 = find_db_size(s35_k, s35_l, 1000, s35_score, 1E-5)
        s35_dbsize_maxsize_e10 = find_db_size(s35_k, s35_l, 1000, s35_score, 1E-10)
        
        print "%s\t%.2f\t%.2f\t%E\t%E" % (l, s35_h * s35_l * l, hoxd70_h * hoxd70_l * l, s35_dbsize_maxsize_e5, s35_dbsize_maxsize_e10)

if __name__ == "__main__":
    main()

