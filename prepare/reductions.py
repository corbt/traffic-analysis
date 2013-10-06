def group_by_time(groups, incident):
	"""Groups incident reports into buckets of 3-hour increments"""
	time = incident['start']
	key = "{yr}-{month}-{day}-{period}".format(yr=time.year, month=time.month, day=time.day, period=time.hour//3)
	# groups[key].append(incident)
	groups[key].append(incident)
	return groups