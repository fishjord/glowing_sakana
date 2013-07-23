#!/usr/bin/env python

import subprocess
import sys
import os
import shutil

if len(sys.argv) != 7:
    print >>sys.stderr, "USAGE: primer_check.py <path/to/probematch.jar> <path/to/ReadSeq.jar> <path/to/weblogo> <primers file> <aligned_nucl_file> <errors>"
    sys.exit(1)

probematch_jar = sys.argv[1]
readseq_jar = sys.argv[2]
weblogo = sys.argv[3]
primers_file = sys.argv[4]
nucl_file = sys.argv[5]
max_errors = int(sys.argv[6])
dealign = os.path.join(os.path.split(os.path.realpath(__file__))[0], "dealign.py")

print "#primer_name\tnum_seqs\t{0}\ttotal".format("\t".join([str(x) for x in range(max_errors + 1)]))
for line in open(primers_file):
    if line[0] == "#":
        continue
    lexemes = line.strip().split()

    primer_name = lexemes[0]
    search_primer = lexemes[2]
    nucl_start = lexemes[3]
    nucl_end = lexemes[4]

    primer_seqfile = "primer_{0}.fasta".format(primer_name)
    primer_aligned_seqfile = "primer_{0}_aligned.fasta".format(primer_name)
    trimmed_seqfile = "trimmed_{0}".format(nucl_file)
    logo_file = "primer_{0}.png".format(primer_name)

    cmd = ["java", "-cp", readseq_jar, "edu.msu.cme.rdp.readseq.utils.SequenceTrimmer", "-i", "--length", "{0}".format(len(search_primer) - max_errors), nucl_start, nucl_end, nucl_file]
    subprocess.check_call(cmd)
    out = open(primer_seqfile, "w")
    subprocess.check_call([dealign, trimmed_seqfile], stdout=out)
    out.flush()
    out.close()

    num_seqs = int(subprocess.check_output(["grep", "-c", ">", primer_seqfile]))
    shutil.move(trimmed_seqfile, primer_aligned_seqfile)
    subprocess.check_call([weblogo, "--fin", primer_aligned_seqfile, "--fout", logo_file, "--format", "png"])

    cmd = ["java", "-jar", probematch_jar, search_primer, primer_seqfile, str(max_errors)]
    error_counts = {}
    for line in subprocess.check_output(cmd).split("\n"):
        if len(line) == 0 or line[0] == "#":
            continue

        lexemes = line.strip().split("\t")
        if len(lexemes) != 6:
            print lexemes
            continue

        errors = int(lexemes[4])
        error_counts[errors] = error_counts.get(errors, 0) + 1

    errors_array = [error_counts.get(errors, 0) for errors in range(max_errors + 1)]
    print "{0}\t{1}\t{2}\t{3}".format(primer_name, num_seqs, "\t".join(["{0}".format(errors) for errors in errors_array]), sum(errors_array))
    print "{0}\t{1}\t{2}\t{3}".format(primer_name, num_seqs, "\t".join(["{0:.3f}".format(errors / float(num_seqs)) for errors in errors_array]), "{0:.3f}".format(sum(errors_array) / float(num_seqs)))

