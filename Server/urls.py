# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

from .Webhandler import IndexHandler
from .Webhandler import LoginHandler
from .Sockethandler import GameHandler

urls = [
    (r"/", IndexHandler),
    (r"/reg", LoginHandler),
    (r"/login", LoginHandler),
    (r"/game", GameHandler),
]