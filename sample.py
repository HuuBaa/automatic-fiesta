#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
from tornado.options import define,options
define('port',default=8000,help='使用 --port 输入的端口号',type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('sample2.html')

class SampleModule(tornado.web.UIModule):
    def render(self, sample):
        return self.render_string(
            "modules/sample.html",
            sample=sample
        )

    def html_body(self):
        return "<div class=\"addition\"><p>html_body()</p></div>"

    def embedded_javascript(self):
        return "document.write(\"<p>embedded_javascript()</p>\")"

    def embedded_css(self):
        return ".addition {color: #A1CAF1}"

    def css_files(self):
        return "/static/css/sample.css"

    def javascript_files(self):
        return "/static/js/sample.js"

if __name__=="__main__":
    tornado.options.parse_command_line()
    app=tornado.web.Application(
        handlers=[
            (r'/',IndexHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__),'templates'),
        ui_modules={'Sample':SampleModule}
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()