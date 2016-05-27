#encoding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

from hashlib import sha1
import os
import time
import redis

from tornado.options import define, options
define('port', default=80, help="run on the given port", type=int)

session_container = {}
create_session_id = lambda: sha1( '%s%s' %(os.urandom(16), time.time()) ).hexdigest()

"""
class SessionManager(object):
  def __init__(self, redis_host, redis_port=6379, redis_passwd=None):
    if redis_passwd:
      self.redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_passwd)
    else:
      self.redis = redis.StrictRedis(host=redis_host, port=redis_port)

  def set(self, id, key, value):
    self.redis.hset(id, key, value)

  def get(self, id, key):
    return self.redis.hget(id, key)

  def del(self, id, key):
    self.redis.
"""
class Session(object):
  session_id = '__SESSIONID__'

  def __init__(self, request):
    session_value = request.get_secure_cookie(Session.session_id)
    if not session_value:
      self._id = create_session_id()
      request.set_secure_cookie(Session.session_id, self._id)
    else:
      self._id = session_value
    print self._id

  def __getitem__(self, key):
    try:
      return session_container[self._id][key]
    except:
      return None

  def __setitem__(self, key, value):
    if session_container.has_key(self._id):
      session_container[self._id][key] = value
    else:
      session_container[self._id] = {key:value}

  def __delitem__(self, key=None):
    if key:
      del session_container[self._id][key]
    else:
      del session_container[self._id]

  def clear_all_session(self, request):
    self.__delitem__()
    request.clear_all_cookies()

class BaseHandler(tornado.web.RequestHandler):
  def initialize(self):
    self.my_session = Session(self)

  def get_current_user(self):
    try:
      return self.my_session['is_login']
    except:
      return None

class LoginHandler(BaseHandler):
  def get(self):
    if not self.my_session['is_login']:
      self.render('login.html')
    else:
      self.redirect(self.get_argument('next', '/'))

  def post(self):
    username = self.get_argument('username')
    password = self.get_argument('password')
    if username == 'google' and password == 'yahoo':
      self.my_session['c_user'] = username
      self.my_session['c_card'] = password
      self.my_session['is_login'] = True
      self.redirect('/')
    else:
      self.render('login.html')

class LogoutHandler(BaseHandler):
  def get(self):
    if self.my_session['is_login']:
      self.my_session.clear_all_session(self)
    self.redirect('/')

class MainHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    print self.my_session['c_user']
    print self.my_session['c_card']
    self.write('Welcome Index')

if __name__ == '__main__':
  tornado.options.parse_command_line()
  settings = {
    'template_path':    'templates',
    'static_path':      'static',
    'static_url_path':  '/static/',
    'xsrf_cookies':     True,
    'cookie_secret':    'LiRbdCfp3yCLMjRiWp7qTA+mF8CWOhCXWD6eZH/2p+ANy/O7ISULoEfDT78m4iUBwYh+HO0hcmrL',
    'debug':            True,
    'login_url':        '/login'
  }

  application = tornado.web.Application([
    (r'/',  MainHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
  ], **settings)

  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
