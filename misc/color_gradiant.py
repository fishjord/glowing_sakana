#!/usr/bin/env python

import sys

if len(sys.argv) != 4:
	print "USAGE: color_gradiant.py <r,g,b> <r,g,b> <steps>"
	sys.exit(1)

first_color = [int(x) for x in sys.argv[1].split(",")]
second_color = [int(x) for x in sys.argv[2].split(",")]

if len(first_color) != 3:
	print "First color doesn't have 3 parts"
	sys.exit(1)
if len(second_color) != 3:
	print "Second color doesn't have 3 parts"
	sys.exit(1)

steps = int(sys.argv[3])

middle = int((steps / 2.0) + .5)

step = [first_color[0] / middle, first_color[1] / middle, first_color[2] / middle]

colors = []

for i in range(0, middle):
	colors.append([first_color[0] - step[0] * i, first_color[1] - step[1] * i, first_color[2] - step[2] * i])

step = [second_color[0] / middle, second_color[1] / middle, second_color[2] / middle]

for i in range(0, middle):
	colors.append([step[0] * i, step[1] * i, step[2] * i])

print "c(%s)" % (",".join(["\"#%02x%02x%02x\"".upper() % (c[0], c[1], c[2]) for c in colors]))
