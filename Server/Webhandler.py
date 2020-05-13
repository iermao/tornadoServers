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


class IndexHandler(RequestHandler):
    def get_current_user(self):
        '''
        重写RequestHandler类中的get_current_user方法，用来判断当前是否是登录状态，请求中所有被@tornado.web.authenticated 装饰的方法，都需要此方法返回值不为None，否则给与403拒绝
        :return: 用户名或者None . 为None判断为非法请求，POST 时Tornado进行403 禁止访问 ；GET 时 302 重定向到/login  123213213
        '''
        user = self.get_argument(name='username', default='None')
        if user and user != 'None':
            print('IndexHandler类 get_current_user获取到用户:', user)
            return user

    @tornado.web.authenticated
    # 确认请求合法 依赖于get_current_user(self):函数的返回值作为判断请求是否合法
    def get(self):
        print("IndexHandler 收到GET请求")
        self.render("online_index.html", current_user=self.current_user)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        print('IndexHandler 收到POST请求')
        self.render("online_index.html", current_user=self.current_user)


class LoginHandler(RequestHandler):

    acc = Account()

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
        await self.write(self.msg)

    # @tornado.gen.coroutine
    async def post(self, *args, **kwargs):
        '''
        暂时用不到
        :param args:
        :param kwargs:
        :return:
        '''
        _data = self.request.body
        print(_data)
        # print(self.acc.POOL)
        msg = await self.acc.Reg(_data, self)
        msgjson = json.loads(msg)
        self.write(msgjson)
        self.finish()
        # print("222")
