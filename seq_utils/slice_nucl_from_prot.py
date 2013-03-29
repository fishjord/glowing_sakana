#!/usr/bin/python

import os
from Bio import SeqIO

full_seq_dict = dict()
for seq in SeqIO.parse(open("/work/fishjord/other_projects/protein_processing/pipeline/resources/buk/framebot.fasta"), "fasta"):
	full_seq_dict[str(seq.id)] = str(seq.seq)

nucl_seq_dict = dict()
for seq in SeqIO.parse(open("buk_nucl_to_slice.fasta"), "fasta"):
	nucl_seq_dict[str(seq.id)] = str(seq.seq)

for seq in SeqIO.parse(open("buk_sliced_prot.fasta"), "fasta"):
	prot_seq = full_seq_dict[str(seq.id)]
	nucl_seq = nucl_seq_dict[str(seq.id)]

	sliced_seq = str(seq.seq)

	start = prot_seq.index(sliced_seq)
	end = start + len(sliced_seq)

	nucl_start = start * 3
	nucl_end = end * 3

	print ">%s\n%s" % (seq.id, nucl_seq[nucl_start:nucl_end])


