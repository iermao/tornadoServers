# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os
import sys
import tornado
from tornado.websocket import WebSocketHandler

from .WebSocket.Game import game

from tornado import gen
# 继承tornado.websocket.WebSocketHandler,只处理WS协议的请求


class CurrentUser(object):
    def __init__(self, _uid, _pwd, _keys):
        self.uid = ""
        self.pwd = ""
        self.keys = ""
        self.cid = 0


class GameHandler(WebSocketHandler):

    # print('start arg 2:', str(sys.argv))
    game = game()

    def get_current_user(self):
        uid = self.get_argument(name='uid', default='None')
        pwd = self.get_argument(name='pwd', default='None')
        keys = self.get_argument(name='keys', default='None')

        currentuser = CurrentUser(uid, pwd, keys)
        currentuser.uid = uid
        currentuser.pwd = pwd
        currentuser.keys = keys

        if currentuser.uid != None:
            return currentuser
        else:
            return None

    # @tornado.web.authenticated
    async def open(self):
        print('WebSocket open')
        # if(self.close)
        state, msg = await self.game.NewUser(self)
        if state == False:
            await self.close()

    # 接收消息
    async def on_message(self, message):
        await self.game.ServerMsg(self, message)

    # 关闭连接
    @gen.coroutine
    def on_close(self):
        # print("on_close1")
        yield self.game.close(self)
        # print("on_close2")

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
