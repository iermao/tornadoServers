# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os
import tornado
import time

from tornado import gen

from tornado.options import define, options

from tornado.websocket import WebSocketHandler

define("port", type=int, default=8001, help="run on the given port")


class Puser():
    async def __init__(self):
        pass


class Game():
    users = set()

    async def __init__(self):
        self.id = 1
        _puser = await Puser()

    async def ServerMsg(self, msg):
        pass

    async def NewUser(self, user):
        await self.sleep(user)
        print("sleep")
        await self.sleep2(user)
        # if (user in self.users):
        #     _puser = await Puser()
        #     print("1111111")
        #     pass
        # else:
        #     self.users.add(user)
        pass

    async def sleep(self, user):
        await gen.sleep(2)
        if (int(user.current_user) == 2):
            print("sleep 1", user.current_user)
            await gen.sleep(4)
            await self.sleep2(user)
            print("sleep 2", user.current_user)
        pass

    async def sleep2(self, user):
        print("sleep2", user.current_user)
        pass


class GameHandler(WebSocketHandler):

    game = Game()

    def get_current_user(self):
        uid = self.get_argument(name='username', default='None')

        if uid != None:
            return uid
        else:
            return None

    async def open(self):
        # print('收到新的WebSocket连接')
        # print("111", self.current_user)
        await self.game.NewUser(self)
        # print("222", self.current_user)

    # 接收消息
    async def on_message(self, message):
        await self.game.ServerMsg(self, message)

    # 关闭连接

    async def on_close(self):
        await self.close()

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


urls = [
    (r"/game", GameHandler),
]


class app():
    def __init__(self):
        print("app __ini__")
        self.AppStart()

    def AppStart(self):

        options.parse_command_line()  # 允许命令行启动程序
        app = tornado.web.Application(
            urls,
            websocket_ping_interval=5,
            static_path=os.path.join(os.path.dirname(__file__), "statics"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            login_url='/login',
            # xsrf_cookies=False,
            # cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
            debug=True,
        )
        http_server = tornado.httpserver.HTTPServer(app)  # 将应用处理逻辑 传递给HTTPServer 服务
        http_server.listen(options.port)  # 配置监听地址到 HTTPServe
        print("websocket server run port = {0}".format(options.port))

        tornado.ioloop.IOLoop.current().start()  # 启动应用


if __name__ == '__main__':
    print("11111111")
    app()
