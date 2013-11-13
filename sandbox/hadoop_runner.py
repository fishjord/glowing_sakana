#!/usr/bin/env python

import os
import subprocess
import sys
import time

reducers = 10

hadoop_cmd = "/home/hadoop/hadoop-0.18.3/bin/hadoop"
jarlibs = "/scratch/fishjord/Clustering/lib/ReadSeq.jar,/scratch/fishjord/Clustering/lib/AlignmentRetrieval.jar"
jobjar = "/scratch/fishjord/Clustering/Clustering.jar"

def main(seq_file, id_mapping, dist_cutoff, run_name, mask_seq):
	bin_seq_file = run_name + "_seqs.bin"
	hadoop_bin_seq_file = run_name + "/" + bin_seq_file
	sample_dir = run_name + "/sampling"
	matrix_dir = run_name + "/matrix"

	if not os.path.exists(bin_seq_file):
		print "Converting sequences to binary format"

		cmd = ["cafe", "-Xmx4g", "ClusterMain", "hadoop", "bin-seqs", seq_file, id_mapping, bin_seq_file]
		if mask_seq:
			cmd.append(mask_seq)

		subprocess.check_call(cmd)
	else:
		print "Binary sequence file exists (%s), manually remove if you want it to be recreated" % bin_seq_file

	subprocess.call([hadoop_cmd, "fs", "-ls", run_name])

	sys.stdout.write("Putting binary sequence file on hdfs [this will delete any files previously in %s on hdfs, press ^C to stop] in " % run_name)

	for i in range(5, 0, -1):
		sys.stdout.write("%s..." % i)
		sys.stdout.flush()
		time.sleep(1)

	print

	subprocess.call([hadoop_cmd, "fs", "-rmr", run_name])
	subprocess.call([hadoop_cmd, "fs", "-mkdir", run_name])
	subprocess.check_call([hadoop_cmd, "fs", "-put", bin_seq_file, hadoop_bin_seq_file])

	print "Running sampling"
	cmd = [hadoop_cmd, "jar", "-libjars", jarlibs, jobjar, "hadoop", "sample", dist_cutoff, "1", "10", hadoop_bin_seq_file, sample_dir]
	subprocess.check_call(cmd, env={"HADOOP_HEAPSIZE" : "12000"})

	print "Running distance matrix"
	cmd = [hadoop_cmd, "jar", "-libjars", jarlibs, jobjar, "hadoop", "dmatrix", dist_cutoff, "1", sample_dir + "/part-00000", hadoop_bin_seq_file, matrix_dir, str(reducers), "true"]
	subprocess.check_call(cmd)

	print "Clustering..."
	cmd = [hadoop_cmd, "jar", "-libjars", jarlibs, jobjar, "hadoop", "cluster", "-m", run_name + "_merges.bin"]
	cmd.extend([matrix_dir + "/part-%05d" % x for x in range(0, reducers)])
	print " ".join(cmd)

	subprocess.check_call(cmd, env={"HADOOP_HEAPSIZE" : "7000"})

if __name__ == "__main__":
	if len(sys.argv) != 5 and len(sys.argv) != 6:
		print "USAGE: hadoop_helper.py <seq_file> <id-mapping> <dist-cutoff> <run-name> [mask-seq-name]"
	else:
		if len(sys.argv) == 6:
			main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
		else:
			main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], None)
