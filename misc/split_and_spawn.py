#!/usr/bin/python

import os
import sys
import shutil
import subprocess
import time
import re
from Bio import SeqIO

not_num_regex = re.compile("[^\d]+")

class Command:
	def __init__(self, cmd, stdout=None):
		self.cmd = cmd
		self.stdout = stdout
		
def run_commands(cmds, trace, distributed=False, workdir=os.getcwd()):
	jids = []
	for cmd in cmds:
		if distributed:
			qsub = ["qsub", "-e", "/dev/null", "-b", "y", "-wd", workdir]
			if cmd.stdout:
				qsub.extend(["-o", cmd.stdout])

			qsub.extend(cmd.cmd)

			trace.write(" ".join(qsub) + "\n")
			trace.flush()
			qsub_stdout = subprocess.Popen(qsub, stdout=subprocess.PIPE).communicate()[0]
			#print qsub_stdout.strip()

			jids.append(re.sub(not_num_regex, "", qsub_stdout))
		else:
			out = sys.stdout

			trace.write(" ".join(cmd.cmd))
			if cmd.stdout != None:
				out = open(cmd.stdout, "w")
				trace.write(" > " + cmd.stdout)
			trace.write("\n")
			trace.flush()

			subprocess.check_call(cmd.cmd, stdout=out, cwd=workdir)

			if out != sys.stdout:
				out.close()

	if distributed and len(jids) != 0:
		qsub = ["qsub", "-sync", "y", "-b", "y", "-wd", workdir, "-o", "/dev/null", "-e", "/dev/null", "-hold_jid", ",".join(jids), "echo"]
#		subprocess.check_call(qsub)
		"""So there is this annoying problem where sometimes the queue master becomes unresponsive...so basically if it exits it's done...tabun"""
		subprocess.call(qsub, stdout=subprocess.PIPE)
		trace.write(" ".join(qsub) + "\n")
		trace.flush()

def split_seq_file(f, max_seqs, workdir, suffix):
	print max_seqs
	file_count = 0
	ret_files = []
	seqs = []
	for seq in SeqIO.parse(open(f), "fasta"):
		seqs.append(seq)
		if len(seqs) > max_seqs:
			out_file = os.path.join(workdir, str(file_count) + "_" + suffix)
			out = open(out_file, "w")
			SeqIO.write(seqs, out, "fasta")
			out.close()
			seqs = []
			ret_files.append(out_file)
			file_count = file_count + 1

	if len(seqs) > 0:
		out_file = os.path.join(workdir, str(file_count) + "_" + suffix)
		out = open(out_file, "w")
		SeqIO.write(seqs, out, "fasta")
		out.close()
		file_count = file_count + 1
		ret_files.append(out_file)

	return ret_files

def cat_files(in_files, out):
	if len(in_files) == 0:
		raise Exception("Attemtping to cat together no files!")

	out_stream = open(out, "w")
	
	cmd = ["cat"]
	cmd.extend(in_files)

	subprocess.check_call(cmd, stdout=out_stream)
	out_stream.close()

def main(seq_file, max_seqs, user_cmd):
	cmd_template = []
	param_map = dict()
	
	split_dir = os.path.abspath("splits")
	os.mkdir(split_dir)
	for i in range(len(user_cmd)):
		lexeme = user_cmd[i]
		
		if os.path.exists(lexeme):
			if lexeme != os.path.abspath(lexeme):
				print "Converting %s to absolute path %s" % (lexeme, os.path.abspath(lexeme))
			cmd_template.append(os.path.abspath(lexeme))
		elif lexeme[0] == '{' and lexeme[-1] == '}':
			param_map[lexeme[1:-1]] = i
			cmd_template.append(lexeme)
		elif ":" in lexeme:
			print "I'm guessing this is a classpath...I'll try to resolve the jars to abs paths"
			new_cp = []
			for jar in lexeme.split(":"):
				if os.path.exists(jar):
					new_cp.append(os.path.abspath(jar))
				else:
					new_cp.append(jar)
					
			cmd_template.append(":".join(new_cp))
		else:
			cmd_template.append(lexeme)
	
	print "Commnd template: %s" % (" ".join(cmd_template))
	print "Param map: %s" % param_map
		
	seq_file_splits = split_seq_file(seq_file, max_seqs, split_dir, "seq_file")
	print "Split %s in to %s splits containing at most %s seqs" % (seq_file, len(seq_file_splits), max_seqs)
	
	out_file_map = dict()
	for k in param_map.keys():
		if k == "seq_file":
			continue
		out_file_map[k] = []
	out_file_map["stdout.txt"] = []
	
	cmds = []
	for i in range(len(seq_file_splits)):
		split_file = seq_file_splits[i]
		cmd = list(cmd_template)
		
		for out_file in out_file_map:
			split = os.path.join(split_dir, "%s_%s" % (i, out_file))
			out_file_map[out_file].append(split)
			if out_file != "stdout.txt":
				cmd[param_map[out_file]] = split
		
		cmd[param_map["seq_file"]] = seq_file_splits[i]
		cmds.append(Command(cmd, out_file_map["stdout.txt"][-1]))

	start = time.time()
	trace = open("trace.txt", "w")
	run_commands(cmds, trace, True)
	trace.close()
	print "Commands finished in %ss" % (time.time() - start)
	
	for out_file in out_file_map:
		cat_files(out_file_map[out_file], out_file)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "USAGE: <seq_file> <max_seqs_per_file> <cmd>"
		print "\t<cmd> must contain one instance of '{seq_file}' that will be replaced with the split"
		print "\tfile when spawned to gridware, and every instance of {<file name>} will be treated as an output"
	else:
		main(sys.argv[1], int(sys.argv[2]), sys.argv[3:])
