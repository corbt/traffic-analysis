# Data filters.  Each filter should take one incident and return "true" for
# inclusion or "false" for exclusion.

# An example filter that removes all incidents of severity 4
def bad_filter(incident):
  if 'severity' in incident and incident['severity'] == 4:
    return False
  return True
