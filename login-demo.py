#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path
from tornado.options import define,options
define('port',default=8000,help='使用 --port 输入的端口号',type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index3.html',username=self.current_user)

class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')
    def post(self, *args, **kwargs):
        self.set_secure_cookie('username',self.get_argument('username'))
        self.redirect(self.get_argument('next','/'))

class LogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie('username')
        self.redirect('/')


if __name__=="__main__":
    tornado.options.parse_command_line()
    setting={
        'template_path':os.path.join(os.path.dirname(__file__),'templates'),
        'cookie_secret':'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
        'xsrf_cookies':True,
        'login_url':'/login',
    }
    app=tornado.web.Application(
        handlers=[
            (r'/',IndexHandler),
            (r'/login',LoginHandler),
            (r'/logout',LogoutHandler)
        ],
        **setting,
        debug=True
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()