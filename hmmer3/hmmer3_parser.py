#!/usr/bin/python

#                                                                 --- full sequence ---- --- best 1 domain ---- --- domain number estimation ----
# target name        accession  query name             accession    E-value  score  bias   E-value  score  bias   exp reg clu  ov env dom rep inc description of target
#------------------- ----------   -------------------- ---------- --------- ------ ----- --------- ------ -----   --- --- --- --- --- --- --- --- ---------------------
class hmmer3_parser:
    def __init__(self, s):
        self.stream = s
        if not isinstance(s, file):
            raise TypeError("Excepted file handle")

    def __iter__(self):
        return self

    def next(self):
        while True:
            line = self.stream.readline()
            if line == "":
                raise StopIteration

            line = line.strip()
            lexemes = line.split()

            if line[0] != "#" and len(lexemes) == 19:
                break

        return {"target" : lexemes[0], "target_accession" : lexemes[1], "query" : lexemes[2], "query_accession" : lexemes[3], "eval" : float(lexemes[4]), "score" : float(lexemes[5]), "bias" : float(lexemes[6]), "dom_eval" : float(lexemes[7]), "dom_score" : float(lexemes[8]), "dom_bias" : float(lexemes[9]), "target_desc" : lexemes[18] }
