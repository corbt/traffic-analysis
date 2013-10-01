import json
import filters, transforms

def prepare(file):
  # These functions should be defined in transforms.py
  applied_transforms = [
    "normalize_dates",
    # Add transforms here
    # "flatten_data"
  ]

  # These functions should be defined in filters.py
  applied_filters = [
    "bad_filter",
  ]

  data = json.load(open(file))

  # Apply selected transforms
  for i in xrange(len(data)-1, -1, -1):
    
    for transform in applied_transforms:
      try:
        data[i] = getattr(transforms, transform)(data[i])
      except:
        print "Transformation '%s' failed for incident %i"%(transform, data[i]['incidentId'])

  # Apply selected filters
  for fltr in applied_filters:
    try:
      data = filter(getattr(filters, fltr), data)
    except:
      print "Filter '%s' failed"%(fltr)

  return data