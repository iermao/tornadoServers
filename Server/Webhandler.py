# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os
import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.web import RequestHandler
from Server.Web.Accountmanage import Account

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

    # @tornado.web.authenticated
    # 确认请求合法 依赖于get_current_user(self):函数的返回值作为判断请求是否合法
    async def get(self):
        self.write("get")

    # @tornado.web.authenticated
    async def post(self, *args, **kwargs):
        self.write("post")
        # print('IndexHandler 收到POST请求')
        # self.render("online_index.html", current_user=self.current_user)


class LoginHandler(BaseHandler):

    acc = Account()

    def set_default_headers(self):
        self.allowMyOrigin()

    async def get(self, *args, **kwargs):
        '''
        处理输入昵称界面get请求
        :param args:
        :param kwargs:
        :return:
        '''
        # cookie_value = self.get_secure_cookie('count')
        # print('cookie_value :', cookie_value)
        # count = int(cookie_value) + 1 if cookie_value else 1
        # self.set_secure_cookie("count",
        #                        str(count))  # 设置一个带签名和时间戳的cookie，防止cookie被伪造。

        # 使用ajax方法做的前端
        # self.render('login_use_ajax.html')
        # 使用form表单提交数据 的前端
        # self.render('login_use_form.html')
        print("get")
        await self.write("err")

    # @tornado.gen.coroutine
    async def post(self, *args, **kwargs):
        '''
        暂时用不到
        :param args:
        :param kwargs:
        :return:
        '''
        _data = self.request.body
        # print("post begin :", _data)
        # print(self.acc.POOL)
        msg = await self.acc.Reg(_data, self)
        # print("post end :", msg)
        msgjson = json.loads(msg)
        self.write(msgjson)
        # self.write("11111")
        self.finish()
        # print("222")
    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
