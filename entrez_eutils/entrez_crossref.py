#!/usr/bin/python

import urllib2
import sys
from xml.dom.minidom import parseString

if len(sys.argv) != 4:
    print >>sys.stderr, "USAGE: entrez_crossref.py <dbfrom> <dbto> <id_file>"
    sys.exit(1)

dbfrom = sys.argv[1]
dbto = sys.argv[2]

url_base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=%s&db=%s&id=" % (dbfrom, dbto)

for line in open(sys.argv[3]):
    id = line.strip()

    url = url_base + id
    response = urllib2.urlopen(url)
    response.getcode()

    if response.getcode() != 200:
        print >>sys.stderr, "Failed to fetch %s" % (id)
        continue

    doc = parseString(response.read())
    for linkset in doc.getElementsByTagName("LinkSetDb"):
        name = linkset.getElementsByTagName("LinkName")[0].firstChild.data
        for link in linkset.getElementsByTagName("Id"):
            print "%s\t%s\t%s\t%s\t%s" % (id, dbfrom, dbto, name, link.firstChild.data)
