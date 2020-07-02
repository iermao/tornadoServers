# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

from .Webhandler import IndexHandler
from .Webhandler import LoginHandler
from .Sockethandler import GameHandler

from .Webhandler import ptHandler
urls = [

    # //网站请求
    (r"/", IndexHandler),
    (r"/reg", LoginHandler),
    (r"/login", LoginHandler),
    (r"/login", LoginHandler),
    (r"/pt/.*", ptHandler),
    # //游戏的请求
    (r"/game", GameHandler),
]