import requests, json

regions = [
	"london",
	"stockholm",
	"slc",
	"seattle",
	"sf",
	"la",
	"nyc",
	"berlin",
	"paris"
]

for region in regions:
	print "Pulling data for region {0}".format(region)
	data = requests.get("http://corbt.com/478/{0}.json".format(region)).text.encode('utf-8')
	
	j = json.loads(data)
	pretty_j = json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))

	with open("data/{0}.json".format(region), "w") as f:
	  f.write(pretty_j)
