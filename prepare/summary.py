from collections import OrderedDict

def summarize_groups(group):
  """Returns summary statistics for a group of incidents"""
  summary = OrderedDict()
  first = group[0]

  summary['period']   = first['start'].hour//3
  summary['weather']  = most_common(map(lambda x: x['weather']['current_observation']['weather'], group))
  summary['day']      = first['start'].weekday()

  if summary['day'] in [5, 6]:
    summary['weekend'] = True
  else:
    summary['weekend'] = False

  summary['count'] = len(group)

  return fix_spaces(summary)

def most_common(lst):
  """Calculates the mode of a list"""
  return max(set(lst), key=lst.count)

def fix_spaces(group):
  """Removes spaces from attribute values for Weka"""
  for attribute, value in group.iteritems():
    if isinstance(value, basestring):
      group[attribute] = value.replace(" ","-")
  return group
