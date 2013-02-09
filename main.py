#!/usr/bin/env python
__author__  =   "Akshay Kannan"

import prober
import models

import webapp2 as webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

''' Servlet Classes- Keep strings here hardcoded for easy readability '''
class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        page = None
        monitors = models.get_monitors()
        if user and "dashboard" in self.request.path:
            page = template.render("templates/dashboard.html", {"page": 1, "logout": users.create_logout_url("/"), "user": user, 
                                                                "monitors": monitors,
                                                                "datapoint_dict": [monitor.get_datapoints() for monitor in monitors]})
        elif user:
            page = template.render("templates/monitors.html", {"page": 0, "logout": users.create_logout_url("/"), "user": user, "monitors": monitors})
        else:
           page = template.render("templates/index.html", {"login": users.create_login_url(self.request.uri)}) 
        self.response.out.write(page)

    def post(self):
        user = users.get_current_user()
        action = self.request.get("action")
        if action == "add":
            monitor = models.Monitor(name=self.request.get("name"), user=user, url=self.request.get("url"))
            monitor.save()
            self.redirect("/")
        if action == "delete":
            monitor = models.Monitor.get_by_id(int(self.request.get("key")))
            monitor.delete()
            self.redirect("/")

class PingPage(webapp.RequestHandler):
    def get(self):
        prober.update_all()

application = webapp.WSGIApplication(
        [('/', MainPage),
         ('/dashboard', MainPage), 
         ('/ping', PingPage)], debug=True) # Set this to false before deploying
