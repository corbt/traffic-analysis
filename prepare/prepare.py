from __future__ import division
import sys, json, inspect
from pprint import pprint
from collections import defaultdict
import filters, maps, reductions, summary

def prepare(file, conf):
  data = json.load(open(file))

  # Apply selected maps
  for transform in conf['maps']:
    map_fn = getattr(maps, transform)
    num_args = len(inspect.getargspec(map_fn).args)

    for i in xrange(len(data)-1, -1, -1):      
      try:
        if num_args == 1:
          data[i] = map_fn(data[i])
        elif num_args == 2:
          data[i] = map_fn(i, data)
      except:
        print "Transformation '%s' failed for incident %s..."%(transform, str(data[i])[0:100])

  # Apply selected filters
  for fltr in conf['filters']:
    try:
      data = filter(getattr(filters, fltr), data)
    except:
      print "Filter '%s' failed"%(fltr)

  return data

if __name__ == "__main__":
  print "Prepare preview"
  data = prepare("../data/traffic/sf_bayview.json", json.load(open("../conf/example.json")))
  print len(data)
  print [d['traffic_level'] for d in data[0:6]]
  print data[-1]['previous_traffic']
  print data[-1]['traffic_level']