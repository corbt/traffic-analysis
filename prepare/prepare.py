from __future__ import division
import sys, json
from pprint import pprint
from collections import defaultdict
import filters, maps, reductions, summary

def prepare(file):
  # These functions should be defined in maps.py
  applied_maps = [
    "normalize_dates",
    # Add maps here
    # "flatten_data"
  ]

  # These functions should be defined in filters.py
  applied_filters = [
    "has_weather"
  ]

  data = json.load(open(file))

  # Apply selected maps
  for i in xrange(len(data)-1, -1, -1):
    
    for transform in applied_maps:
      try:
        data[i] = getattr(maps, transform)(data[i])
      except:
        print "Transformation '%s' failed for incident %i"%(transform, data[i]['incidentId'])

  # Apply selected filters
  for fltr in applied_filters:
    try:
      data = filter(getattr(filters, fltr), data)
    except:
      print "Filter '%s' failed"%(fltr)

  # Compute expected number of entries
  first_day = min([incident['start'] for incident in data])
  last_day = max([incident['start'] for incident in data])
  expected = (last_day-first_day).days*8

  # Bin data
  # data = reduce(reductions.group_by_time, data, defaultdict(list))

  # Compute summary statistics
  # data = [summary.summarize_groups(v) for v in data.itervalues()]

  print "{0} entries expected, {1} found. {2}%".format(expected, len(data), len(data)/expected*100)

  return data

if __name__ == "__main__":
  print "Prepare preview"
  data = prepare(sys.argv[1])
  pprint(sorted(data.iteritems()))
