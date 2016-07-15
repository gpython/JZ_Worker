#encoding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import time
import sys
import uuid
import hmac
import ujson
import hashlib
import redis
from tornado.web import HTTPError

from tornado.options import define, options
define('port', default=8080, help="run on the given port", type=int)

class SessionData(dict):
  def __init__(self, session_id, hmac_key):
    self.session_id = session_id
    self.hmac_key = hmac_key

# @property
# def sid(self):
#   return self.session_id
# @x.setter
# def sid(self, value):
#   self.session_id = value

class Session(SessionData):
  def __init__(self, session_manager, request_handler):

    self.session_manager = session_manager
    self.request_handler = request_handler
#

    try:
      current_session = session_manager.get(request_handler)
    except InvalidSessionException:
      current_session = session_manager.get()
    for key, data in current_session.iteritems():
      self[key] = data
    self.session_id = current_session.session_id
    self.hmac_key = current_session.hmac_key
    print self

  def save(self):
    print self
    self.session_manager.set(self.request_handler, self)

  def clear(self):
    self.session_manager.clear(self.request_handler, self)


class SessionManager(object):
  def __init__(self, secret, store_options, session_timeout):
    self.secret = secret
    self.session_timeout = session_timeout
    try:
      if store_options['redis_pass']:
        self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'], password=store_options['redis_pass'])
      else:
        self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'])
    except Exception as e:
      print e


  def _fetch(self, session_id):
    try:
      session_data = raw_data = self.redis.get(session_id)
      if raw_data != None:
        print "Set timeout", self.session_timeout
        self.redis.setex(session_id, self.session_timeout, raw_data)
        session_data = ujson.loads(raw_data)

      if type(session_data) == type({}):
        return session_data
      else:
        return {}
    except IOError:
      return {}

  def get(self, request_handler = None):
    if (request_handler == None):
      session_id = None
      hmac_key = None
    else:
      session_id = request_handler.get_secure_cookie("session_id")
      hmac_key = request_handler.get_secure_cookie("verification")

    if session_id == None:
      session_exists = False
      session_id = self._generate_id()
      hmac_key = self._generate_hmac(session_id)
    else:
      session_exists = True

    check_hmac = self._generate_hmac(session_id)
    if hmac_key != check_hmac:
      raise InvalidSessionException()

    session = SessionData(session_id, hmac_key)

    if session_exists:
      session_data = self._fetch(session_id)
      for key, data in session_data.iteritems():
        session[key] = data
    return session

  def set(self, request_handler, session):
    request_handler.set_secure_cookie("session_id", session.session_id)
    request_handler.set_secure_cookie("verification", session.hmac_key)
    print '*'*10, session.items()
    session_data = ujson.dumps(dict(session.items()))
    self.redis.setex(session.session_id, self.session_timeout, session_data)

  def clear(self, request_handler, session):
    request_handler.clear_all_cookies()
    session_data = ujson.dumps(dict(session.items()))
#    print session_data

    self.redis.delete(session.session_id)

  def _generate_id(self):
    new_id = hashlib.sha256(self.secret + str(uuid.uuid4()))
    return new_id.hexdigest()

  def _generate_hmac(self, session_id):
    return hmac.new(session_id, self.secret, hashlib.sha256).hexdigest()

class InvalidSessionException(Exception):
  pass

"""
def login_required(f):
  def _wrapper(self,*args, **kwargs):
    print self.get_current_user()
    logged = self.get_current_user()
    if logged == None:
      self.write('no login')
      self.finish()
    else:
      ret = f(self,*args, **kwargs)
  return _wrapper
"""
class BaseHandler(tornado.web.RequestHandler):
  def __init__(self, *argc, **argkw):
    super(BaseHandler, self).__init__(*argc, **argkw)
    self.session = Session(self.application.session_manager, self)

  def get_current_user(self):
    try:
      return self.session['is_login']
    except:
      return None

class MainHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    print self.session['c_user']
    print self.session['c_card']
    self.write('Welcome Index')


class LoginHandler(BaseHandler):
  def get(self):
    if not self.session.get('is_login', None):
      self.render('login.html')
    else:
      self.redirect('/')

  def post(self):
    username = self.get_argument('username')
    password = self.get_argument('password')
    if username == 'google' and password == 'yahoo':
      self.session['c_user'] = username
      self.session['c_card'] = password
      self.session['is_login'] = True
      self.session.save()
      print self.session
      self.redirect('/')
    else:
      self.render('login.html')

class LogoutHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    self.session['is_login'] = None
    self.session.save()
    self.session.clear()
    self.redirect('/')

class Application(tornado.web.Application):
  def __init__(self):
    settings = dict(
      template_path =    'templates',
      static_path  =     'static',
      static_url_path =  '/static/',
      xsrf_cookies =     True,
      debug =            True,
      login_url =        '/login',
      cookie_secret = "e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
      session_secret = "3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
      session_timeout = 60,

      store_options = {
      'redis_host': '192.168.47.20',
      'redis_port': 6379,
      'redis_pass': '',
    },)
    handlers = [
      (r"/", MainHandler),
      (r"", MainHandler),
      (r"/login", LoginHandler),
      (r"/logout", LogoutHandler),
    ]
    tornado.web.Application.__init__(self, handlers, **settings)
    self.session_manager = SessionManager(settings["session_secret"], settings["store_options"], settings["session_timeout"])

if __name__ == '__main__':
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
