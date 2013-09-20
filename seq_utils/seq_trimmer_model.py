#trimms sequences from HMM aligned file
# usage: seq_trimmer_model.py  -s 226 -e 336 -m 100  aligned.fasta sliced.fa

#!/usr/bin/python

from Bio import SeqIO
from optparse import OptionParser
import sys
import os
import re

upper_regex = re.compile("[^A-Z]")
base_regex = re.compile("[^A-Za-z]")
refseq_ID = "#=GC_RF"

def chop_end(seqs, model_end, min_modelpositions):	
	chop_seq_dict = dict()
	
	refseq = seqs[refseq_ID]
	model_pos = 0
	model_map = dict()
	for i in range(len(refseq.seq)):
		if refseq.seq[i] != ".":
			model_pos += 1
			model_map[model_pos] = i

	seq_end = model_map[model_end]
	
	for seqid in seqs.keys():
		seq = seqs[seqid]
		## slice from the end
		seqstr = str(seq.seq)[0: seq_end]
		
		if seqid != refseq_ID:
		# check if the upper case chars( model position) pass the minimum requirement
			if len(re.subn(upper_regex, "", seqstr)[0]) >= min_modelpositions:
				chop_seq_dict[seqid] =  seqstr
				
			else:	
				print "%s length %s  %s" % (seq.id, len(re.subn(upper_regex, "", seqstr)[0]), re.subn(upper_regex, "", seqstr)[0])
				pass
		else:
			chop_seq_dict[seqid] = seqstr
	return chop_seq_dict

def chop_begin(seqs, model_start, min_modelpositions):	
	chop_seq_dict = dict()
	
	refseq = seqs[refseq_ID]
	model_pos = 0
	model_map = dict()
	for i in range(len(refseq.seq)):
		if refseq.seq[i] != ".":
			model_pos += 1
			model_map[model_pos] = i

	seq_start = model_map[model_start]
	
	for seqid in seqs.keys():
		seq = seqs[seqid]
		## slice from the begining
		seqstr = str(seq.seq)[seq_start: len(seq.seq)]
		if seqid != refseq_ID:
			# check if the upper case chars( model position) pass the minimum requirement
			if len(re.subn(upper_regex, "", seqstr)[0]) >= min_modelpositions:
				chop_seq_dict[seqid] = seqstr
			else:	
				#print ">%s failed \n%s\n" % (seq.id,re.subn(upper_regex, "", seqstr)[0])
				print "%s" % (seq.id)
				pass
			
		else:
			chop_seq_dict[seqid] = seqstr
			
	return chop_seq_dict	
	
	
def write(chop_seq_dict, outfile):
	output = open(outfile, 'w')
	for seqid in sorted(chop_seq_dict.keys()):
		if seqid != refseq_ID:
			output.write( ">%s\n%s\n" % (seqid, chop_seq_dict.get(seqid)) )	
	output.write( ">#=GC_RF\n%s\n" % (chop_seq_dict.get(refseq_ID) ))
	output.close()		

def write_unalign(chop_seq_dict, outfile):
	output = open(outfile, 'w')
	print "write unaligned"
	for seqid in sorted(chop_seq_dict.keys()):
		seqstr = chop_seq_dict.get(seqid)
		if seqid != refseq_ID:
			output.write( ">%s\n%s\n" % (seqid, re.subn(base_regex, "", seqstr)[0] ))	

	seqstr = chop_seq_dict.get(refseq_ID)
	output.write( ">#=GC_RF\n%s\n" % (re.subn(base_regex, "", seqstr)[0] ))	
	
	output.close()

def chop_both(seqs, model_start, model_end, min_modelpositions, keepshort):
	chop_seq_dict = dict()
	
	refseq = seqs[refseq_ID]
	model_pos = 0
	model_map = dict()
	for i in range(len(refseq.seq)):
		if refseq.seq[i] != ".":
			model_pos += 1
			model_map[model_pos] = i

	seq_start = model_map[model_start]
	seq_end = model_map[model_end] 

	for seqid in seqs.keys():
		seq = seqs[seqid]
		seqstr = str(seq.seq)[seq_start:seq_end +1]
		
		if seqid != refseq_ID:
			## if the sequence does  not cover the beginning, do not output
			temBeforelen = len(re.subn(upper_regex, "", str(seq.seq)[0:seq_start+1])[0])
			tempAfterlen = len(re.subn(upper_regex, "", str(seq.seq)[seq_end-1: len(seq.seq)])[0])
			#temBeforelen = len(re.subn(base_regex, "", str(seq.seq)[0:seq_start+1])[0])
			#tempAfterlen = len(re.subn(base_regex, "", str(seq.seq)[seq_end-1: len(seq.seq)])[0])
			
			
			if  temBeforelen == 0 or tempAfterlen == 0:
				#print ">%s\n%s\n##%s\n" % (seq.id,str(seq.seq)[0:seq_start], str(seq.seq)[seq_end-1:len(seq.seq)])
				if (keepshort):
					if len(re.subn(upper_regex, "", seqstr)[0]) >= min_modelpositions:
						chop_seq_dict[seqid] =  seqstr
				else:
					print "short %s\t%s" % (seq.id, seqstr)
					continue
			
			#if len(re.subn(upper_regex, "", seqstr)[0]) >= min_modelpositions:
			if len(re.subn(base_regex, "", seqstr)[0]) >= min_modelpositions:
				chop_seq_dict[seqid] =  seqstr
			else:				
				print "short %s\t%s" % (seq.id, seqstr)
				pass
			
		else:
			chop_seq_dict[seqid] = seqstr
	return chop_seq_dict



if __name__ == "__main__":
	usage="usage: %prog [options] aligned_seq_file outfile "
	
	parser = OptionParser(usage=usage)
	parser.add_option("-s", "--start", dest="start_model_pos", help="start model position to be included")
	parser.add_option("--stockholm", dest="stockholm", default=False, action="store_true", help="Input is in stockholm format")
	parser.add_option("-e", "--end", dest="end_model_pos", help="end model position to be included")
	parser.add_option("-u", "--unalign", dest="unaligned", help="unaligned format, default is aligned")
	parser.add_option("-m", "--min_modelpositions", dest="min_modelpositions", help="minimum number of model positions required, default is 0")
	parser.add_option("-k", "--keep", dest="keep_short", default= False, action="store_true", help="keep the short sequence even it does not cover the entire region. default is false")

	
	(options, args) = parser.parse_args()
	if len(args) != 2:
		parser.error("Incorrect number of arguments")
	#print "arguments: %s\t%s" %(options, args)

	if options.stockholm:
		import StringIO
		instream = StringIO.StringIO(open(args[0]).read().replace("#=GC RF", "GC_RF"))
		seqs = SeqIO.to_dict(SeqIO.parse(instream, "stockholm"))
		refseq_ID="GC_RF"
	else:
		seqs = SeqIO.to_dict(SeqIO.parse(open(args[0], "fasta")))

	min_modelpositions = 0
	keepshort = False
	if options.keep_short:
		keepshort = True
	if options.min_modelpositions:
		min_modelpositions = int(options.min_modelpositions)
	if options.start_model_pos:
		if not options.end_model_pos:
			chop_seq_dict = chop_begin(seqs, int(options.start_model_pos), min_modelpositions)
		else:
			chop_seq_dict = chop_both(seqs, int(options.start_model_pos), int(options.end_model_pos), min_modelpositions, keepshort)
	elif options.end_model_pos:
		chop_seq_dict = chop_end(seqs, int(options.end_model_pos), min_modelpositions)
	else:
		parser.error("Incorrect number of arguments, expect either the start_model_pos or/and end_model_pos")
	if options.unaligned:
		write_unalign(chop_seq_dict, args[1])
	else:
		write(chop_seq_dict, args[1])
