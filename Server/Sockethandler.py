# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os
from tornado.websocket import WebSocketHandler

from .WebSocket.Game import game

# 继承tornado.websocket.WebSocketHandler,只处理WS协议的请求


class CurrentUser(object):
    uid = ""
    pwd = ""
    keys = ""
    cid = 0

    def __init__(self):
        pass


class GameHandler(WebSocketHandler):

    game = game()

    def get_current_user(self):
        uid = self.get_argument(name='uid', default='None')
        pwd = self.get_argument(name='pwd', default='None')
        keys = self.get_argument(name='keys', default='None')

        currentuser = CurrentUser()
        currentuser.uid = uid
        currentuser.pwd = pwd
        currentuser.keys = keys

        if currentuser.uid != None:
            return currentuser
        else:
            return None

    # @tornado.web.authenticated
    def open(self):
        # print('收到新的WebSocket连接')
        state, msg =  self.game.NewUser(self)
        if state == False:
            print(msg)
            self.close()

    # 接收消息
    def on_message(self, message):
        self.game.ServerMsg(self, message)

    # 关闭连接
    def on_close(self):
        self.game.close(self)

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
