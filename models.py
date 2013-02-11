from google.appengine.ext import db

import time

DATA_LIMIT = 1000

class Monitor(db.Model):
  name = db.StringProperty(required=True)
  user = db.UserProperty(required=True)
  url = db.StringProperty(required=True)
  regexp = db.StringProperty()
  active = db.BooleanProperty(default=True)
  breakcache = db.BooleanProperty(default=True)
  def get_datapoints(self):
    return DataPoint.all().filter("monitor =", self).order("time").fetch(limit=DATA_LIMIT)

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

def get_percent(numerator, denominator):
  try:
    return str(float(numerator) / denominator * 100)[0:6]
  except:
    return str(0.0)

def get_monitoring_data():
  out = []
  index = 0
  for monitor in get_monitors():
    data = {"datapoints": [], 
            "uptimes": [], 
            "outages": None,
            "status": None, 
            "id": index, 
            "name": monitor.name}
    uptime_count = 0
    total_count = 0
    outages = []
    last_status = True
    #populate these variables
    for datapoint in monitor.get_datapoints():
      time = datapoint.get_time()
      data["datapoints"].append(
        {'x': time, 'y': int(datapoint.latency)})
      if not datapoint.success:
        if last_status: outages.append(datapoint.time)
      else:
        uptime_count += 1
      total_count += 1
      last_status = datapoint.success
    #store them
    data["uptimes"].append(get_percent(uptime_count, total_count))
    data["outages"] = [outages.pop() for i in range(0, min(3, len(outages)))]
    data["status"] = last_status
    out.append(data)
    index += 1
  return out
