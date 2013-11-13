#!/usr/bin/env python

import urllib2
import os
import sys
import time

if len(sys.argv) != 4 and len(sys.argv) != 5:
	print "USAGE: fetch_genome_xml.py <db> <genome_id_list> <out_dir> [ret_mode]"
	sys.exit(1)

db = sys.argv[1]
id_file = sys.argv[2]
out_dir = sys.argv[3]
url_template = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=%s&id=%s"

if len(sys.argv) == 5:
	ret_mode = sys.argv[4]
else:
	ret_mode = "xml"

if ret_mode == "fasta":
	url_template += "&rettype=fasta&retmode=text"
elif ret_mode == "xml":
	url_template += "&retmode=xml"
else:
	print >>sys.stderr, "Unknown result type '%s'" % ret_mode
	sys.exit(1)

print url_template

for id in open(id_file):
	id = id.strip()
	if id == "":
		continue

	sys.stdout.write("Fetching %s..." % id)
	sys.stdout.flush()
	out_file = os.path.join(out_dir, "%s.%s" % (id, ret_mode))
	if os.path.exists(out_file):
		print "already fetched"
		continue

	try:
		response = urllib2.urlopen(url_template % (db, id))
		response.getcode()
		if response.getcode() != 200:
			print "Failed, %s" % response.getcode()
			continue

		open(out_file, "w").write(response.read())
		print "Done"
	except Exception as e:
		if os.path.exists(out_file):
			os.unlink(out_file)
		print "Failed: %s" % e
	time.sleep(1.0/3)
