# Data filters.  Each filter should take one incident and return "true" for
# inclusion or "false" for exclusion.

# An example filter that removes all incidents of severity 4
def bad_filter(incident):
  if 'severity' in incident and incident['severity'] == 4:
    return False
  return True

def has_weather(incident):
	if 'weather' in incident and 'current_observation' in incident['weather']:
		return True
	return False

def localize(incident):
	box = ((51.406,-.297),(51.627,.00962))
	lat = incident['point']['coordinates'][0]
	long = incident['point']['coordinates'][1]
	if lat >= box[0][0] and lat <= box[1][0] and long >= box[0][1] and long <= box[1][1]:
		return True
	return False

def exclude_holidays(incident):
	"""Excludes November 27-30 because of possible holiday traffic"""
	if incident['time'].month == 11 and incident['time'].day in [27, 28, 29, 30]:
		return False
	return True