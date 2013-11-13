#!/usr/bin/env python

import os
import sys
import shutil

if len(sys.argv) != 2:
	print "USAGE: seperate_test_sources.py <project_directory"
	sys.exit(1)

project_dir = sys.argv[1]
src_dir = os.path.join(project_dir, "src")
test_dir = os.path.join(project_dir, "test")

if not src_dir.endswith("/"):
	src_dir += "/"

for root, dirs, files in os.walk(src_dir):
	for f in files:
		if f.endswith("Test.java") or f.endswith("TestSuite.java") or f.endswith("Suite.java"):
			path = root.replace(src_dir, "")
			source_file = f
			target = os.path.join(os.path.join(test_dir, path), source_file)

			print "Moving %s (path= %s) to %s" % (source_file, path, target)
			if not os.path.exists(os.path.split(target)[0]):
				os.makedirs(os.path.split(target)[0])
			shutil.move(os.path.join(root, f), target)

	if '.svn' in dirs:
	    dirs.remove('.svn')  # don't visit CVS directories
