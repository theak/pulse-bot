from google.appengine.ext import db

import time

DATA_LIMIT = 100

class Monitor(db.Model):
  name = db.StringProperty(required=True)
  user = db.UserProperty(required=True)
  url = db.StringProperty(required=True)
  regexp = db.StringProperty()
  def get_datapoints(self):
    return self.datapoint_set.order('time').fetch(limit=DATA_LIMIT)

class DataPoint(db.Model):
  monitor = db.ReferenceProperty(Monitor)
  success = db.BooleanProperty(required=True)
  latency = db.IntegerProperty(required=True)
  time = db.DateTimeProperty(auto_now=True)
  def get_time(self):
    return int(time.mktime(self.time.timetuple()))
  def get_up(self):
    return 100 if self.success else 0

def get_monitors():
  return Monitor.all().fetch(limit=DATA_LIMIT)
