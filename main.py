#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

import os
import random
from collections import defaultdict

from tornado.options import define,options
define('port',default=8000,help='使用 --port 输入的端口号',type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index2.html')

class ChangePageHandler(tornado.web.RequestHandler):
    def source_to_map(self,text):
        mapped=defaultdict(list)
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x)>0]:
                if word[0] not in mapped:
                    mapped[word[0]].append(word)
        return mapped

    def post(self, *args, **kwargs):
        source_text=self.get_argument('source_text')
        change_text=self.get_argument('change_text')
        source_map=self.source_to_map(source_text)
        change_lines=change_text.split('\r\n')
        self.render('poem2.html',source_map=source_map,change_lines=change_lines,choice=random.choice)



if __name__=="__main__":
    tornado.options.parse_command_line()
    app=tornado.web.Application(
        handlers=[
            (r'/',IndexHandler),
            (r'/poem',ChangePageHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__),'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=True
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()