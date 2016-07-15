#encoding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import redis
from session import Session, SessionManager

from tornado.options import define, options
define('port', default=8080, help="run on the given port", type=int)

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
      cookie_secret = "erfI2CItqdJG2AA1su5103panMMlr05ZmamQXSf3OPoq0Bury1YteKtHPAmA+TxWtrTnVNTrOevT==",
      session_secret = "OLza01dzGmWXf0V910zynJ4IkrYtR74GWi4pXwR8ZY/DssIhIRPV7CrVY4XclVYdHoAZCCIQtQB==",
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
