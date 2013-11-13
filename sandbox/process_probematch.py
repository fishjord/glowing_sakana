#!/usr/bin/env python

import sys
from Bio import SeqIO

def read_probe_file(probe_file):
	ret = dict()

	for line in open(probe_file):
		lexemes = line.strip().split("\t")
		if len(lexemes) != 4:
			continue

		if lexemes[0] not in ret:
			ret[lexemes[0]] = list()
		ret[lexemes[0]].append([int(x) for x in lexemes[1:3]])

	return ret

def main(seq_file, fprimer_file, rprimer_file):
	seqs = SeqIO.to_dict(SeqIO.parse(open(seq_file), "fasta"))

	fprimer_hits = read_probe_file(fprimer_file)
	rprimer_hits = read_probe_file(rprimer_file)

	for seqid in fprimer_hits.keys():
		if seqid not in seqs or seqid not in rprimer_hits:
			sys.stderr.write("%s\tNo matching rprimers\n" % seqid)
			continue

		for fprimer in fprimer_hits[seqid]:
			best_rprimer = None
			best_score = 100000

			new_seq_id = "%s_fprimer_%s" % (seqid, fprimer[0])

			for rprimer in rprimer_hits[seqid]:
				if rprimer[0] < fprimer[1]:
					continue
				if best_rprimer == None or rprimer[0] - fprimer[1] < best_score:
					best_rprimer = rprimer
					best_score = rprimer[0] - fprimer[1]

			if best_rprimer == None:
				sys.stderr.write("%s\tNo rprimers before forward primer %s\n" % (seqid, fprimer[0]))
				continue

			sys.stderr.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (seqid, new_seq_id, fprimer[0], fprimer[1], best_rprimer[0], best_rprimer[1], best_score))

			sys.stdout.write(">%s\n%s\n" % (new_seq_id, seqs[seqid].seq[fprimer[1]:best_rprimer[0]]))

if __name__ == "__main__":
	if len(sys.argv) == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print "USAGE: process_probematch.py <seq_file> <fprimer_file> <rprimer_file>"
