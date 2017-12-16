#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define,options
define('port',default=8000,help='使用 --port 输入的端口号',type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('index')
    def post(self):
        pass
    def write_error(self, status_code, **kwargs):
        self.write('Sorry!You caused a %s error.'%status_code)


if __name__=="__main__":
    tornado.options.parse_command_line()
    app=tornado.web.Application(
        handlers=[
            (r'/',IndexHandler)
        ]
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()