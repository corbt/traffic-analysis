import sys, json
from pprint import pprint
from collections import defaultdict
import filters, maps, reductions

def prepare(file):
  # These functions should be defined in maps.py
  applied_maps = [
    "normalize_dates",
    # Add maps here
    # "flatten_data"
  ]

  # These functions should be defined in filters.py
  applied_filters = [
    # "localize",
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

  # Bin data
  data = reduce(reductions.group_by_time, data, defaultdict(list))

  # Compute summary statistics
  data = [maps.summarize_groups(v) for v in data.itervalues()]

  return data

if __name__ == "__main__":
  print "Prepare preview"
  data = prepare(sys.argv[1])
  pprint(sorted(data.iteritems()))