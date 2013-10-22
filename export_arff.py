# Example usage: python export_arff.py data/test.json test.arff

import sys
import arff, requests
from prepare import prepare

# This function takes a JSON list of incidents, processes them, and exports an ARFF file
def export_arff(file, export_file):
  data = prepare.prepare(file)

  # Structure of export
  export_data = {
    'attributes': [],
    'data': [],
    'relation': 'TrafficData'
  }

  leave_numeric = [
    "count"
  ]

  # print data
  attributes = data[0].keys()
  for attr in attributes:
    if attr not in leave_numeric:
      vals = list(set([incident[attr] for incident in data]))
      export_data['attributes'].append((attr, vals))
    else:
      export_data['attributes'].append((attr, 'INTEGER'))

  for incident in data:
    entry = []
    for attr in attributes:
      if attr in incident:
        entry.append(incident[attr])
      else:
        entry.append('?')
    export_data['data'].append(entry)

  with open(export_file, "w") as f:
    f.write(arff.dumps(export_data))


if __name__ == "__main__":
  if len(sys.argv) > 1:
    export_arff(sys.argv[1],sys.argv[2])
  else:
    # data = requests.get("http://corbt.com/478/sf.json")
    # with open("data/latest.json", "w") as f:
    #   f.write(data.text)
    export_arff("data/latest.json", "latest.arff")