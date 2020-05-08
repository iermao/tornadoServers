# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os

import tornado.web
import tornado.ioloop
import tornado.httpserver

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
        state, msg = self.game.NewUser(self)
        if state == False:
            print(msg)
            self.close()

    # 接收消息
    def on_message(self, message):
        self.game.ServerMsg(self, message)
        # message = json.loads(message)
        # print(type(message), message)
        # print(self.current_user)
        # print("------" + str(len(self.users)))
        # for u in self.users:  # 向在线用户广播消息
        #     u.write_message(
        #         u"[%s]-[%s]-说：<br> &nbsp&nbsp&nbsp&nbsp%s" %
        #         (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #          self.current_user, message.get('msg')))

    # 关闭连接

    def on_close(self):
        self.game.close(self)
        # self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        # for u in self.users:
        #     u.write_message(u"[%s]-[%s]-%s 离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.current_user))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
