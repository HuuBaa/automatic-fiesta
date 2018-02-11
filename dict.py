#!/usr/bin/env python
#-*- coding: utf-8 -*-
#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from pymongo import MongoClient
import json
from tornado.options import define,options
define('port',default=8000,help='使用 --port 输入的端口号',type=int)


class Application(tornado.web.Application):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.example
        handlers = [(r'/(\w+)', IndexHandler)]
        tornado.web.Application.__init__(self,handlers=handlers,debug=True)


class IndexHandler(tornado.web.RequestHandler):
    def get(self,word):
        dic=self.application.db.words.find_one({'word':word})
        if dic:
            del dic['_id']
            self.write(dic)
        else:
            self.set_status(404)
            self.write({'error':'word not find'})

    def post(self,word):
        definition=self.get_argument('definition')
        coll=self.application.db.words
        dic=coll.find_one({'word':word})
        if dic:
            dic['definition']=definition
            coll.save(dic)
        else:
            coll.insert({'word':word,'definition':definition})

        dic = coll.find_one({'word': word})
        del dic['_id']
        print(json.dumps(dic))
        self.write(dic)

if __name__=="__main__":
    tornado.options.parse_command_line()

    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()