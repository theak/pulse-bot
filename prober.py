import models

from time import time
from google.appengine.api.urlfetch import fetch

#return unix time in ms
def ms_time():
  return int(time() * 1000)

#take in a url, regexp (optional) and return (success, latency)
#todo: regexp support not yet implemented
def test(url, regexp):
  start_time = ms_time()
  try:
    fetch(url)
  except:
    return False, ms_time() - start_time
  return True, ms_time() - start_time

def update(monitor):
  success, latency = test(monitor.url, monitor.regexp)
  datapoint = models.DataPoint(monitor=monitor, success=success, latency=latency)
  datapoint.save()

def update_all():
  for monitor in models.get_monitors():
    update(monitor)
