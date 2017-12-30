#!/usr/bin/env python
#-*- coding: utf-8 -*-


import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

import os

from tornado.options import options,define
define('port',8000,help='使用--port设置端口',type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')

class PoemHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        n1=self.get_argument('noun1')
        n2 = self.get_argument('noun2')
        v1 = self.get_argument('verb1')
        n3 = self.get_argument('noun3')
        self.render('poem.html',n1=n1,n2=n2,v1=v1,n3=n3)

if __name__=='__main__':
    tornado.options.parse_command_line()
    app=tornado.web.Application(
        handlers=[(r'/',IndexHandler),(r'/poem',PoemHandler)],
        template_path=os.path.join(os.path.dirname(__file__),'templates'),
        debug=True
                                )

    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()