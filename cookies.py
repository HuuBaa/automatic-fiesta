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
        cookie=self.get_secure_cookie("count")
        print(cookie)
        count=int(cookie)+1 if cookie!=b'None' else 1
        self.set_secure_cookie("count",str(count))
        self.write('你浏览了这个页面%s次'%count)

    def write_error(self, status_code, **kwargs):
        self.write('Sorry!You caused a %s error.'%status_code)


if __name__=="__main__":
    tornado.options.parse_command_line()
    settings={
        "cookie_secret":"5AbDGuLRTVCM7W5sLQ4kmhPLTihZ/E/qnXXnzAYIH8M="
    }
    app=tornado.web.Application(
        handlers=[
            (r'/',IndexHandler)
        ],
        debug=True
        ,
        **settings
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

