from __future__ import division
import sys, json
from pprint import pprint
from collections import defaultdict
import filters, maps, reductions, summary

def prepare(file, conf):
  data = json.load(open(file))

  # Apply selected maps
  for i in xrange(len(data)-1, -1, -1):
    
    for transform in conf['maps']:
      try:
        data[i] = getattr(maps, transform)(data[i])
      except:
        print "Transformation '%s' failed for incident %s..."%(transform, str(data[i])[0:100])

  # Apply selected filters
  for fltr in conf['filters']:
    try:
      data = filter(getattr(filters, fltr), data)
    except:
      print "Filter '%s' failed"%(fltr)

  # # Code for binning
  # # Compute expected number of entries
  # first_day = min([incident['start'] for incident in data])
  # last_day = max([incident['start'] for incident in data])
  # expected = (last_day-first_day).days*8

  # # Bin data
  # data = reduce(reductions.group_by_time, data, defaultdict(list))

  # # Compute summary statistics
  # data = [summary.summarize_groups(v) for v in data.itervalues()]

  # print "{0} entries expected, {1} found. {2}%".format(expected, len(data), len(data)/expected*100)

  return data

if __name__ == "__main__":
  print "Prepare preview"
  data = prepare("../data/sf.json", json.load(open("../conf/example.json")))
  print len(data)