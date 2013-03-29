#!/usr/bin/python

import sys

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

if len(sys.argv) != 4:
	print "USAGE: split_seqs.py <in_seqs> <# seqs per file> <out_dir>"
	sys.exit(1)

split_seq_file(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[1])
