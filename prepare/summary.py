from collections import OrderedDict

def summarize_groups(group):
  """Returns summary statistics for a group of incidents"""
  summary = OrderedDict()
  first = group[0]

  summary['period']   = first['start'].hour//3
  summary['weather']  = mode([x['weather']['current_observation']['weather'] for x in group])
  summary['temperature'] = mean([x['weather']['current_observation']['feelslike_f'] for x in group])
  summary['day']      = first['start'].weekday()

  if summary['day'] in [5, 6]:
    summary['weekend'] = True
  else:
    summary['weekend'] = False

  summary['count'] = len(group)

  return fix_spaces(summary)

def mode(lst):
  """Calculates the mode of a list"""
  return max(set(lst), key=lst.count)

def mean(lst):
  """Calculates the mean of a numeric list"""
  return sum([float(x) for x in lst])/len(lst)

def fix_spaces(group):
  """Removes spaces from attribute values for Weka"""
  for attribute, value in group.iteritems():
    if isinstance(value, basestring):
      group[attribute] = value.replace(" ","-")
  return group
