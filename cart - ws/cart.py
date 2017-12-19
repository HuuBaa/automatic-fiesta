#!/usr/bin/env python
#-*- coding: utf-8 -*-

#/cart/ ajax 添加、删除
#/cart/ststus/ 长轮询api，
#/主页显示

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.websocket
import uuid
from tornado.options import define,options

define('port',8000,help='输入端口',type=int)

class ShopCart(object):
    Inventory=10
    callbacks=[]
    carts={}
    def register(self,callback):
        self.callbacks.append(callback)

    def unregister(self,callback):
        self.callbacks.remove(callback)

    def addCart(self,session):
        if session in self.carts:
            return
        self.carts[session]=True
        self.notifyAll()

    def removeCart(self,session):
        if session not in self.carts:
            return
        del self.carts[session]
        self.notifyAll()

    def getInventory(self):
        return self.Inventory-len(self.carts)

    def notifyAll(self):
        for cb in self.callbacks:
            cb(self.getInventory())


class Application(tornado.web.Application):
    def __init__(self):
        self.shopCart=ShopCart()
        handlers=[
            (r'/',IndexHandler),
            (r'/cart/',CartHandler),
            (r'/cart/status/',StatusHandler)
        ]
        settings=dict(
            template_path='templates',
            static_path='static',
            debug=True
        )
        tornado.web.Application.__init__(self,handlers=handlers,**settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        session=uuid.uuid4()
        count=self.application.shopCart.getInventory()
        self.render('cart.html',count=count,session=session)

class CartHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        session=self.get_argument('session')
        action=self.get_argument('action')
        if not session:
            self.set_status(400)
            return

        if action=='add':
            self.application.shopCart.addCart(session)
        elif action=='remove':
            self.application.shopCart.removeCart(session)
        else:
            self.set_status(400)

class StatusHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.shopCart.register(self.cb)
    def on_message(self, message):
        pass
    def on_close(self):
        self.application.shopCart.unregister(self.cb)
        print('remove cb')
    def cb(self,count):
        self.write_message('{"inventoryCount":"%d"}'%count)

http_server=tornado.httpserver.HTTPServer(Application())
http_server.listen(options.port)
tornado.ioloop.IOLoop.instance().start()