#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import random

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=True)
    consent = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    version = ndb.StringProperty(indexed=True)
    status = ndb.StringProperty(indexed=True)
# [END greeting]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = 'default'
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START guestbook]
class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = 'default'
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
        greeting.content = self.request.get('content')
        greeting.consent = 'True'
        greeting.put()

        self.redirect('/?' + guestbook_name)
# [END guestbook]
class Ctrl(webapp2.RequestHandler):
    def get(self):
        guestbook_name = 'default'
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
        greeting.status = 'V1:INC'
        greeting.put()
        template = JINJA_ENVIRONMENT.get_template('Ctrl.html')
        self.response.write(template.render(what = 'test'))
class CtrlAlmostDone(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('CtrlAlmostDone.html')
        self.response.write(template.render(wa = 'test'))
class CtrlDone(webapp2.RequestHandler):
    def get(self):
        guestbook_name = 'default'
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
        greeting.status = 'V1:COMPLETE'

        greeting.put()
        template = JINJA_ENVIRONMENT.get_template('CtrlDone.html')
        self.response.write(template.render(w = 'test'))
class CtrlCheat(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('CtrlCheat.html')
        self.response.write(template.render(wa = 'test'))
class CtrlCheatDone(webapp2.RequestHandler):
    def get(self):
        guestbook_name = 'default'
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
        greeting.status = 'V1:CHEAT'
        greeting.put()
        template = JINJA_ENVIRONMENT.get_template('CtrlCheatDone.html')
        self.response.write(template.render(w = 'test'))
class Exp(webapp2.RequestHandler):
    def get(self):
        guestbook_name = 'default'
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
        greeting.status = 'V2:INC'
        greeting.put()
        template = JINJA_ENVIRONMENT.get_template('Exp.html')
        self.response.write(template.render(what = 'test'))
class ExpAlmostDone(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('ExpAlmostDone.html')
        self.response.write(template.render(wa = 'test'))
class ExpDone(webapp2.RequestHandler):
    def get(self):
        guestbook_name = 'default'
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
        greeting.status = 'V2:COMPLETE'
        greeting.put()
        template = JINJA_ENVIRONMENT.get_template('ExpDone.html')
        self.response.write(template.render(w = 'test'))
class ExpCheat(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('ExpCheat.html')
        self.response.write(template.render(wa = 'test'))
class ExpCheatDone(webapp2.RequestHandler):
    def get(self):
        guestbook_name = 'default'
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())
        greeting.status = 'V2:CHEAT'
        greeting.put()
        template = JINJA_ENVIRONMENT.get_template('ExpCheatDone.html')
        self.response.write(template.render(w = 'test'))
# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/827sf45', Ctrl),
    ('/736ft2', CtrlAlmostDone),
    ('/23642z', CtrlCheat),
    ('/382sm2', CtrlDone),
    ('/9473zf', CtrlCheatDone),
    ('/2139xi', Exp),
    ('/09128s', ExpAlmostDone),
    ('/1238s', ExpCheat),
    ('/7391kf', ExpDone),
    ('/9652fse', ExpCheatDone)
], debug=True)
# [END app]
