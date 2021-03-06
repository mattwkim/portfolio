#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import logging
import jinja2
from google.appengine.api import mail


# Lets set it up so we know where we stored the template files
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.path == '/':
            template = JINJA_ENVIRONMENT.get_template("templates" + self.request.path + "index.html")
            self.response.write(template.render())
        else:
            if self.request.path == "/contactme":
                template = JINJA_ENVIRONMENT.get_template("templates" + self.request.path + ".html")
                self.response.write(template.render({'hello':'If you would like to contact me, please fill out the form below. '}))                
            else:
                template = JINJA_ENVIRONMENT.get_template("templates" + self.request.path + ".html")
                self.response.write(template.render())
    def post(self):
        if self.request.path == '/':
            template = JINJA_ENVIRONMENT.get_template("templates" + self.request.path + "index.html")
            self.response.write(template.render())
        else:
            if self.request.path == "/contactme":
                template = JINJA_ENVIRONMENT.get_template("templates" + self.request.path + ".html")
                user_address = "mattwkim@umich.edu"
                sender_address = self.request.get("email")
                subject = self.request.get("firstname") + "," + self.request.get("lastname")
                body = "From " + self.request.get("firstname") + " " + self.request.get("lastname") + ",\n" + self.request.get("message")
                mail.send_mail(sender_address, user_address, subject, body)
                self.response.write(template.render({'hello':'Your message has been sent!'}))                
            else:
                template = JINJA_ENVIRONMENT.get_template("templates" + self.request.path + ".html")
                self.response.write(template.render())

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("templates/login.html")
        self.response.write(template.render({'title':'begin'}))
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        if username == "mattwkim" and password == "1029384756Mk":
            template = JINJA_ENVIRONMENT.get_template("templates/loggedin.html")
            self.response.write(template.render({'title':'good'}))
        else:
            logging.info(username + ' is not the correct username.')
            logging.info(password + ' is not the correct password.')
            template = JINJA_ENVIRONMENT.get_template("templates/login.html")
            self.response.write(template.render({'title':'bad'}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/dog', MainHandler),
    ('/contactme', MainHandler),
    ('/index', MainHandler),
    ('/resume', MainHandler),
    ('/login', LoginHandler),
    ('/loggedin', LoginHandler)
    ], debug=True)
