#!/usr/bin/python


def read_id_mapping(stream, int_ids=False, inc=dict()):
    ret = inc
    for line in stream:
        lexemes = line.strip().split()
        if len(lexemes) != 2:
            continue

        seqids = lexemes[1].split(",")
        exemplar = seqids[0]

        if int_ids:
            ret[int(lexemes[0])] = seqids
        else:
            ret[examplar] = seqids

    return ret

def read_sample_mapping(stream, inc=dict()):
    ret = inc
    for line in stream:
        lexemes = line.strip().split()
        if len(lexemes) < 2:
            continue

        ret[lexemes[0]] = lexemes[1]

    return ret
