# Usage: python pull_json.py
# Will pull the SF data by default.
# Optionally can pull other/more areas with "python pull_json.py region1,region2,etc"

import requests, json, sys

regions = ["nyc"]
if len(sys.argv) > 1:
	regions = sys.argv[1].split(",")

for region in regions:
	print "Pulling data for region {0}".format(region)
	data = requests.get("http://corbt.com/478/{0}.json".format(region)).text.encode('utf-8')
	print "\tData downloaded.  Processing"
	j = json.loads(data)
	data = json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))

	with open("data/{0}.json".format(region), "w") as f:
	  f.write(data)