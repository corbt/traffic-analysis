# Example usage: python export_arff.py data/sf.json sf.arff conf/example.conf

import sys
import arff, requests, json, datetime
from jsonpath_rw import parse as jp_parse
from prepare import prepare

def export_arff(file, export_file, conf):
  """Takes a JSON list of incidents, processes them, and exports an ARFF file"""
  conf = json.load(open(conf))
  data = prepare.prepare(file, conf)

  # Structure of export
  export_data = {
    'attributes': [],
    'data': [],
    'relation': 'TrafficData'
  }

  paths = [jp_parse(path[1]) for path in conf['attributes']]

  # print data[0]
  for incident in data:
    entry = []
    for path in paths:
      results = path.find(incident)
      if len(results) > 0:
        if isinstance(results[0].value, basestring):
          entry.append(results[0].value.replace(" ", "-"))
        else:
          entry.append(results[0].value)
      else:
        entry.append(None)
    export_data['data'].append(entry)

  for index,attr in enumerate(conf['attributes']):
    if attr[2] in ['NUMERIC', 'REAL', 'INTEGER']:
      export_data['attributes'].append((attr[0], attr[2]))
    else:
      # Otherwise assume discrete
      vals = list(set([incident[index] for incident in export_data['data']]))
      export_data['attributes'].append((attr[0], vals))

  export_data['description'] = "\n".join(
    [str(datetime.datetime.now()), 
    json.dumps(conf, indent=2, separators=(',', ': '))])

  with open(export_file, "w") as f:
    f.write(arff.dumps(export_data))


if __name__ == "__main__":
  if len(sys.argv) > 1:
    export_arff(sys.argv[1],sys.argv[2],sys.argv[3])
  else:
    export_arff("data/sf.json", "arffs/sf.arff", "conf/example.json")