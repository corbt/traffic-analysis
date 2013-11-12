# Transforms that process the data.  Each transform should take one record and
# return the same record modified.
from __future__ import division
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

def calculate_traffic(incident):
  """Calculates the traffic level at the time of the incident"""
  resources = incident['traffic']['resourceSets'][0]['resources']
  duration_traffic = sum([r['travelDurationTraffic'] for r in resources])/len(resources)
  duration = sum([r['travelDuration'] for r in resources])/len(resources)

  incident['traffic_level'] = (duration_traffic - duration)/duration
  return incident

def flatten(incident):
  """Moves some data to the top level for export"""
  # incident['']  