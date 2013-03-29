import re
import urllib
import demjson
import time

ip_regex = re.compile("\d+\.\d+\.\d+\.\d+")
#base_url = "http://iplocationtools.com/ip_query.php?output=json&ip=";
base_url = "http://api.hostip.info/get_html.php?position=true&ip="

survey_results = open("results.txt", "r")
resolve_file = open("resolved.txt", "w")
#json_file = open("json.txt", "w")

ip_addr_array = list()

for line in open("results.txt", "r"):
        ipaddr = line.split("\t")[1]
        if ip_regex.search(ipaddr) == None:
                continue
	if ipaddr in ip_addr_array:
		continue

	ip_addr_array.append(ipaddr)

print "List contains", len(ip_addr_array), "entries"

#json_file.write("[")
for ipaddr in ip_addr_array:
	resp = urllib.urlopen(base_url + ipaddr).read().replace("?", "").replace("\n", "").replace("(", "").replace(")", "")

	#response = demjson.decode(json)

	match = re.compile("\-?[\d\.]+").findall(resp)

	if len(match) == 2:
		lat = match[0]
		long = match[1]

		resolve_file.write(ipaddr + "\t" + lat + "\t" + long)
	else:
		print "Failed to lookup", ipaddr

	#if response["Status"] == 'OK':
	#	resolve_file.write(response["Latitude"] + "\t" + response["Longitude"])
	#else:
	#	print "Failed to resolve", ipaddr

	resolve_file.write("\n")
	#json_file.write(json + ", ")
	
	time.sleep(5)

#json_file.write("]")
