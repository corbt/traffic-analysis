# Transforms that process the data.  Each transform should take one record and
# return the same record modified.

import re
from datetime import datetime

# Replaces the Javascript-style date objects returned with actual Python dates.
def normalize_dates(incident):
  for date in ['start','end','lastModified']:
    if incident[date]:
      milliseconds = re.findall('\d+',incident[date])
      seconds = int(milliseconds[0])/1000

      incident[date] = datetime.fromtimestamp(seconds)      

  return incident

# Transforms to implement
# Local time
# Local weather
# 