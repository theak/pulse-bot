import models

from time import time
from random import random
from google.appengine.api.urlfetch import fetch

#return unix time in ms
def ms_time():
  return int(time() * 1000)

def break_cache(url):
  rand = str(random())[2:]
  param = "breakcache" + rand + "=" + rand
  return url + ('?' if '?' not in url else '&') + param

#take in a url, regexp (optional) and return (success, latency)
#todo: regexp support not yet implemented
def test(url, regexp, breakcache):
  start_time = ms_time()
  perform_fetch = lambda: fetch(break_cache(url) if breakcache else url)
  try:
    perform_fetch()
  except:
    try:
      perform_fetch() #try again
    except:
      return False, ms_time() - start_time
  return True, ms_time() - start_time

def update(monitor):
  success, latency = test(monitor.url, monitor.regexp, monitor.breakcache)
  datapoint = models.DataPoint(monitor=monitor, success=success, latency=latency)
  datapoint.save()

def update_all():
  for monitor in models.Monitor.all().filter("active =", True):
    update(monitor)
