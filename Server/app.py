# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os
import tornado
# import tornado.ioloop
# import tornado.httpserver
from tornado.options import define, options

from Server import config

define("port", type=int, default=config.ws_point, help="run on the given port")

# from .Webhandler import IndexHandler
# from .Webhandler import LoginHandler

# from .Sockethandler import GameHandler

from . import urls


class app():
    def __init__(self):
        # print("app __ini__")
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
            debug=False,
        )
        http_server = tornado.httpserver.HTTPServer(app)  # 将应用处理逻辑 传递给HTTPServer 服务
        http_server.listen(options.port)  # 配置监听地址到 HTTPServe
        print("websocket server run port = {0}".format(options.port))
        # http_server.start(4)
        tornado.ioloop.IOLoop.instance().start()  # 启动应用


if __name__ == '__main__':
    app()