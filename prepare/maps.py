# Transforms that process the data.  Each transform should take one record and
# return the same record modified.
from __future__ import division
import re
from datetime import datetime
from dateutil import parser

def normalize_dates(incident):
  """Replaces datetime strings with Datetime objects"""
  incident['time'] = parser.parse(incident['time'])
  return incident

def day_and_time(incident):
	"""Extracts the day of the week, hour of the day, and weekday/weekend status"""
	incident['hour'] = incident['time'].hour
	incident['day']  = incident['time'].weekday()

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