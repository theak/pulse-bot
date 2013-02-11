#!/usr/bin/env python
__author__  =   "Akshay Kannan"

import prober
import models

import webapp2 as webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from json import dumps

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        page = None
        monitors = models.get_monitors()
        page_data = {"logout": users.create_logout_url("/"), "user": user, "login": users.create_login_url(self.request.uri)}
        if user and "dashboard" in self.request.path:
            page_data["page"] = 1
            page_data["monitors"] = models.get_monitoring_data()
            page = template.render("templates/dashboard.html", page_data)
        elif user:
            page_data["page"] = 0
            page_data["monitors"] = models.get_monitors()
            page = template.render("templates/monitors.html", page_data)
        else:
           page = template.render("templates/index.html", page_data)
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
        if self.request.get("redirect"): self.redirect("/dashboard")    

application = webapp.WSGIApplication(
        [('/', MainPage),
         ('/dashboard', MainPage), 
         ('/ping', PingPage)], debug=True) # Set this to false before deploying
