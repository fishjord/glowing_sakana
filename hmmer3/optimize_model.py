#!/usr/bin/env python

import subprocess
import sys
import os
import shutil

if len(sys.argv) != 3:
	print "USAGE: optimze_model.py <input_alignment> <passes>"
	sys.exit(1)

passes = int(sys.argv[2])
input_alignment = sys.argv[1]

### File juggling
temp_model_1 = "temp_model1.hmm"
temp_model_2 = "temp_model2.hmm"

unaligned_file = "unaligned_seqs.fasta"

temp_alignment = "temp.sto"

def dealign(infile, outfile):
	out = open("tmp.fasta", "w")
	subprocess.call(["cafe", "ClusterMain", "to-fasta", infile], stdout=out)
	out.close()

	out = open(outfile, "w")
	subprocess.call(["dealign.py", "tmp.fasta"], stdout=out)
	out.close()

	os.remove("tmp.fasta")

### Turn our input alignment in to unaligned sequences for bootstrapping
dealign(input_alignment, unaligned_file)

### Build the initial model
subprocess.check_call(["hmmbuild", temp_model_1, input_alignment])

### Now optimize, it should stabilize over 20 or so passes...but I don't have a measurment, so look at it by hand you lazy ass
for i in range(passes):
	subprocess.check_call(["hmmalign", "-o", temp_alignment, temp_model_1, unaligned_file])
	subprocess.check_call(["hmmbuild", temp_model_2, temp_alignment])

	shutil.move(temp_model_2, temp_model_1)

shutil.move(temp_model_1, ".".join(input_alignment.split(".")[:-1]) + ".hmm")

