#!/usr/bin/env python

from Bio import SeqIO
import sys
import argparse

low_cov = 2
med_cov = 5
high_cov = 10
coverage_colors = { "none" : "red", "low" : "orangered", "medium" : "yellow", "high" : "olivedrab1" }

def parse_ref_kmers(ref_kmer_file, k):
    ref_kmers = {}
    for seq in SeqIO.parse(open(ref_kmer_file), "fasta"):
        seq_str = str(seq.seq).lower()
        for i in range(len(seq.seq) - k + 1):
            ref_kmers[seq_str[i:i+k]] = str(seq.description)

    return ref_kmers

def read_kmer_coverage(cov_file):
    kmer_cov = {}
    for line in open(cov_file):
        lexemes = line.strip().split()
        if len(lexemes) == 0:
            continue

        kmer = lexemes[0]
        kmer_cov[kmer] = len(lexemes) - 1

    return kmer_cov

def read_graph(input_reads, k, ref_kmers, kmer_cov):
    kmers_to_ids = {}

    in_edges = {}
    out_edges = {}

    node_labels = {}
    edge_labels = {}

    node_id = 0

    for seq in SeqIO.parse(open(input_reads), "fasta"):
        seq_str = str(seq.seq).lower()
        last_id = None
        for i in range(len(seq_str) - k + 1):
            kmer = seq_str[i:i+k]

            if kmer not in kmers_to_ids:
                kmers_to_ids[kmer] = node_id
                node_labels[node_id] = {}
                node_labels[node_id]["kmers"] = set([kmer])
                node_labels[node_id]["refids"] = set()
                node_labels[node_id]["seqids"] = set()

                if kmer_cov != None:
                    node_labels[node_id]["cov"] = kmer_cov.get(kmer, 0)

                out_edges[node_id] = []
                in_edges[node_id] = []

                node_id += 1

            id = kmers_to_ids[kmer]
            if kmer in ref_kmers:
                node_labels[id]["refids"].add(ref_kmers[kmer])
            node_labels[id]["seqids"].add(str(seq.description))

            if last_id != None:
                if last_id not in edge_labels:
                    edge_labels[last_id] = {}

                if id not in out_edges[last_id]:
                    out_edges[last_id].append(id)
                    if id not in edge_labels[last_id]:
                        edge_labels[last_id][id] = {}
                    edge_labels[last_id][id]["collapsed"] = 1

                    if kmer_cov != None:
                        edge_labels[last_id][id]["cov"] = min(node_labels[id]["cov"], node_labels[last_id]["cov"])
                if last_id not in in_edges[id]:
                    in_edges[id].append(last_id)

            last_id = id

    return in_edges, out_edges, node_labels, edge_labels

def get_cov_color(cov):
    if cov < low_cov:
        return coverage_colors["none"]
    elif cov < med_cov:
        return coverage_colors["low"]
    elif cov < high_cov:
        return coverage_colors["medium"]
    else:
        return coverage_colors["high"]

def add_dot_kv(k, v, attrs):
    attrs.append("{0}=\"{1}\"".format(k, v))

def format_node(id, node_labels):
    labels = node_labels[id]
    attrs = []
    if "refids" in labels and len(labels["refids"]) > 0:
        label = ", ".join(sorted(labels["refids"]))
    else:
        label = ", ".join(sorted(labels["seqids"]))

    if "cov" in labels:
        label += " cov: {0:.2f}".format(labels["cov"])
        add_dot_kv("color", get_cov_color(labels["cov"]), attrs)

    label = list(labels["kmers"])[0]
    add_dot_kv("label", label, attrs)
    return "\t{0} [{1}];".format(id, ",".join(attrs))

def format_edge(tail, head, edge_labels):
    labels = edge_labels[tail][head]
    attrs = []

    collapsed = labels["collapsed"]
    add_dot_kv("minlen", max(1, collapsed / 10.0 + .5), attrs)

    if "cov" in labels:
        add_dot_kv("label", "nodes: {0}, cov: {1:.2f}".format(collapsed, labels["cov"] / float(collapsed)), attrs)
        add_dot_kv("color", get_cov_color(labels["cov"] / float(collapsed)), attrs)
    else:
        add_dot_kv("label", collapsed, attrs)

    return "\t{0} -> {1} [{2}];".format(tail, head, ",".join(attrs))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref-file", dest="ref_file", help="File containing sequences with 'true' kmers")
    parser.add_argument("--cov-file", dest="cov_file", help="File containing contig kmer abundances (generatable from ContigKmerCounting)")
    parser.add_argument("--low-abund-cutoff", dest="low_abund", help="Kmers with coverage below this value are 'low coverage'", type=int, default=2)
    parser.add_argument("--med-abund-cutoff", dest="low_abund", help="Kmers with coverage below this value are 'medium coverage'", type=int, default=7)
    parser.add_argument("k", help="Kmer size", type=int)
    parser.add_argument("input_reads", help="Contig file")

    args = parser.parse_args()

    if args.ref_file:
        ref_kmers = parse_ref_kmers(args.ref_file, args.k)
    else:
        ref_kmers = {}

    if args.cov_file:
        kmer_cov = read_kmer_coverage(args.cov_file)
    else:
        kmer_cov = None

    in_edges, out_edges, node_labels, edge_labels = read_graph(args.input_reads, args.k, ref_kmers, kmer_cov)

    print "digraph sg {"
    for id in out_edges.keys():
        print format_node(id, node_labels)
        for v in out_edges[id]:
            print format_edge(id, v, edge_labels)

        print

    print "}"

if __name__ == "__main__":
    main()
