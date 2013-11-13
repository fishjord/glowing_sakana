#!/usr/bin/env python

import os
import sys

"""
File(s):	FUSION26_good.fasta 
Sequences:	6828 

distance cutoff:	0.0
Total Clusters:	2780
"""

def clust_cmp(line1, line2):
	count1 = int(line1.split()[2])
	count2 = int(line2.split()[2])

	return cmp(count2, count1)

def clust_cmp2(line1, line2):
	count1 = int(line1.split()[0])
	count2 = int(line2.split()[0])

	return cmp(count1, count2)

def main(in_clust, num_remove, out_clust):
	in_stream = open(in_clust)
	out_stream = open(out_clust, "w")

	line = in_stream.readline()
	lexemes = line.split(":")

	if len(lexemes) != 2 or lexemes[0].strip() != "File(s)":
		print "Malformed files line in %s" % in_clust
		return

	if len(lexemes[1].split()) != 1:
		print "This tool only works with single sample cluster files"
		return

	out_stream.write(line)

	line = in_stream.readline()
	lexemes = line.split(":")

	if len(lexemes) != 2 or lexemes[0].strip() != "Sequences":
		print "Malformed Sequence line in %s" % in_clust
		return

	if len(lexemes[1].split()) != 1:
		print "This tool only works with single sample cluster files"
		return

	out_stream.write(line)
	out_stream.write(in_stream.readline())

	while line != "":
		line = in_stream.readline()
		if line == "":
			break

		lexemes = line.split(":")

		if len(lexemes) != 2 or lexemes[0].strip() != "distance cutoff":
			print "Malformed distance line in %s: %s" % (in_clust, line)
			return

		dist_line = line

		line = in_stream.readline()
		lexemes = line.split(":")

		if len(lexemes) != 2 or lexemes[0].strip() != "Total Clusters":
			print "Malformed Total Clusters line in %s: %s" % (in_clust, line)
			return

		num_clusters = int(lexemes[1].strip())
		if num_clusters <= num_remove:
			print "%s has %d clusters, fewer than %d I'd remove, stopping here" % (dist_line.strip(), num_clusters, num_remove)
			break

		out_stream.write(dist_line)
		out_stream.write("Total Clusters: %d\n" % (num_clusters - num_remove))

		clust_lines = []
		while line.strip() != "":
			line = in_stream.readline()
			if len(line.split()) > 3:
				clust_lines.append(line)

		clust_lines.sort(clust_cmp)
		out_lines = clust_lines[num_remove:]
		out_lines.sort(clust_cmp2)
		for line in out_lines:
			out_stream.write(line)

	out_stream.close()
	in_stream.close()

if __name__=="__main__":
	if len(sys.argv) == 4:
		main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
	else:
		print "USAGE: remove_clusters.py <input_cluster_file> <number_of_clusters_to_remove> <output_cluster_file>"
