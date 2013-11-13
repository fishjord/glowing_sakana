#!/usr/bin/env python

import sys
import struct

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: fourcc_gen.py <fourcc>"
    sys.exit(1)

fourcc = sys.argv[1]
if len(fourcc) > 4:
    print >>sys.stderr, "Length cannot be greater than 4"
    sys.exit(1)

if len(fourcc) < 4:
    fourcc = " " * (4 - len(fourcc)) + fourcc

print fourcc
print "{0:x}".format(struct.unpack(">I", fourcc)[0])
