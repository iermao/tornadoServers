# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os
import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.web import RequestHandler
from Server.Web.Accountmanage import Account
from Server.Web.bytedanceHandler import bytedanceHandler

from tornado import httpclient

import json


class BaseHandler(RequestHandler):
    #  允许跨域访问的地址
    def allowMyOrigin(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')


class IndexHandler(BaseHandler):
    def get_current_user(self):
        '''
        重写RequestHandler类中的get_current_user方法，用来判断当前是否是登录状态，请求中所有被@tornado.web.authenticated 装饰的方法，都需要此方法返回值不为None，否则给与403拒绝
        :return: 用户名或者None . 为None判断为非法请求，POST 时Tornado进行403 禁止访问 ；GET 时 302 重定向到/login  123213213
        '''
        user = self.get_argument(name='username', default='None')
        if user and user != 'None':
            print('IndexHandler类 get_current_user获取到用户:', user)
            return user

    # 确认请求合法 依赖于get_current_user(self):函数的返回值作为判断请求是否合法
    async def get(self):
        self.write("get")

    async def post(self, *args, **kwargs):
        self.write("post")


class LoginHandler(BaseHandler):
    acc = Account()

    def set_default_headers(self):
        self.allowMyOrigin()

    async def get(self, *args, **kwargs):
        print("get")
        self.write("err")

    async def post(self, *args, **kwargs):
        _data = self.request.body
        msg = await self.acc.Reg(_data, self)

        msgjson = json.loads(msg)
        print(self.request.method)
        print(self.request.uri)
        print(self.request.path)
        print(self.request.query)
        print(self.request.version)
        print(self.request.headers)
        print(self.request.body)
        print(self.request.remote_ip)
        print(self.request.protocol)
        print(self.request.host)
        print(self.request.arguments)
        print(self.request.query_arguments)
        print(self.request.body_arguments)
        print(self.request.files)
        print(self.request.connection)
        print(self.request.cookies)
        print(self.request.full_url())
        print(self.request.request_time())

        self.write(msgjson)

        self.finish()

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


# 平台登录等
class ptHandler(BaseHandler):
    bytedance = bytedanceHandler()

    def set_default_headers(self):
        self.allowMyOrigin()

    async def get(self, *args, **kwargs):
        await self.bytedance.get_access_token(self)
        self.finish()

    async def post(self, *args, **kwargs):
        await self.write("post")
        self.finish()

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
