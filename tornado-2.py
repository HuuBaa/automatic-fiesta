import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

import textwrap

from tornado.options import define,options
define('port',default=8000,help='使用 --port 输入的端口号',type=int)

class ReverseHandler(tornado.web.RequestHandler):
    def get(self,input):
        self.write(input[::-1])
    def write_error(self, status_code, **kwargs):
        self.write('Sorry!You caused a %s error.'%status_code)

class TextWrapHandler(tornado.web.RequestHandler):
    def post(self):
        text=self.get_argument('text')
        width=self.get_argument('width',40)
        s=textwrap.fill(text,int(width))
        self.write(s)

if __name__=="__main__":
    tornado.options.parse_command_line()
    app=tornado.web.Application(
        handlers=[
            (r'/reverse/(\w+)',ReverseHandler),
            (r'/wrap',TextWrapHandler)
        ]
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()