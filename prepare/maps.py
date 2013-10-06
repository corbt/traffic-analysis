# Transforms that process the data.  Each transform should take one record and
# return the same record modified.

import re
from datetime import datetime
from collections import OrderedDict

def normalize_dates(incident):
  """Replaces JSON-style dates with Datetime objects"""
  for date in ['start','end','lastModified']:
    if incident[date]:
      milliseconds = re.findall('\d+',incident[date])
      seconds = int(milliseconds[0])/1000

      incident[date] = datetime.fromtimestamp(seconds)      

  return incident

def flatten(incident):
  """Moves some data to the top level for export"""
  # incident['']

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

  return summary

def most_common(lst):
  """Calculates the mode of a list"""
  return max(set(lst), key=lst.count)