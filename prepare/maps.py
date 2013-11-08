# Transforms that process the data.  Each transform should take one record and
# return the same record modified.

import re
from datetime import datetime

def normalize_dates(incident):
  """Replaces JSON-style dates with Datetime objects"""
  for date in ['start','end','lastModified']:
    if incident[date]:
      milliseconds = re.findall('\d+',incident[date])
      seconds = int(milliseconds[0])/1000

      incident[date] = datetime.fromtimestamp(seconds)      

  return incident

def day_and_time(incident):
	"""Extracts the day of the week, hour of the day, and weekday/weekend status"""
	incident['hour'] = incident['start'].hour
	incident['day']  = incident['start'].weekday()

	if incident['day'] in [5, 6]:
	  incident['weekend'] = True
	else:
	  incident['weekend'] = False

	return incident

def flatten(incident):
  """Moves some data to the top level for export"""
  # incident['']  