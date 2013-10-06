# Example usage: python export_arff.py data/test.json test.arff

import sys
import arff
from prepare import prepare

# This function takes a JSON list of incidents, processes them, and exports an ARFF file
def export_arff(file, export_file):
  data = prepare.prepare(file)

  attributes = data[0].keys()
  export_data = []
  for incident in data:
    entry = []
    for attr in attributes:
      if attr in incident:
        entry.append(incident[attr])
      else:
        entry.append('?')
    export_data.append(entry)

  arff.dump(export_file, export_data, relation="TrafficData", names=attributes)

if __name__ == "__main__":
  export_arff(sys.argv[1],sys.argv[2])