#!/usr/bin/python

import os
import sys
import time
from Bio import SeqIO

if len(sys.argv) != 3:
	print "USAGE: kmer_clustering.py <contig_file> <k>"
	sys.exit(1)

kmers_to_clusters = dict()

class Cluster:
	def __init__(self, id):
		self.seqs = set()
		self.kmers = set()
		self.id = id

seq_file = sys.argv[1]
k = int(sys.argv[2])

cluster_count = 1
clusters = dict()

start = time.time()
seqs = SeqIO.to_dict(SeqIO.parse(open(seq_file), "fasta"))

for seq in seqs.values():
        seq_str = str(seq.seq)
	
	kmers = [seq_str[i:i+k] for i in range(len(seq_str) - k + 1)]
	c1 = None

	for kmer in kmers:
		if kmer in kmers_to_clusters:
			c1 = kmers_to_clusters[kmer]
			break

	if c1 == None:
		c1 = Cluster(cluster_count)
		cluster_count += 1
		clusters[c1.id] = c1

	c1.seqs.add(str(seq.id))
	c1.kmers.update(kmers)

	for kmer in kmers:
		merge_clusters = set()
		if kmer in kmers_to_clusters:
			c2 = kmers_to_clusters[kmer]
			if c1.id != c2.id:
				merge_clusters.add(c2.id)

		for cid in merge_clusters:
			c2 = clusters[cid]
			c1.seqs.update(c2.seqs)
			c1.kmers.update(c2.kmers)

			for update_kmer in c2.kmers:
				kmers_to_clusters[update_kmer] = c1

			del clusters[c2.id]

		kmers_to_clusters[kmer] = c1

final_clusters = 0
clustered_seqs = 0

for cid in clusters:
	cluster = clusters[cid]
	clustered_seqs += len(cluster.seqs)
	print "%s\t%s" % (cid, ",".join(cluster.seqs))
	final_clusters += 1

print >>sys.stderr, "Clustered %s sequences in to %s clusters (accounting for %s seqs) sharing at least 1 %smer in %ss" % (len(seqs), final_clusters, clustered_seqs, k, (time.time() - start))

