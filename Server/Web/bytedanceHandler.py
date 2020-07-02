#
# 字节跳动登录相关
#
import json
import time
import hashlib

from Server import logging

import tornado.web
from tornado import gen

from . import dbhelper
from . import CFun

from tornado import httpclient


class bytedanceHandler():
    def __init__(self):
        self.appid = 0
        self.secret = ""
        self.grant_type = "client_credential"
        self.access_token_gettime = 0
        self.access_token = ""

        self.access_token_url = "https://developer.toutiao.com/api/apps/token?appid={0}&secret={1}&grant_type={2}"

        self.login_url = "https://developer.toutiao.com/api/apps/jscode2session?appid={0}&secret={1}&code={2}&anonymous_code={3}"
        pass

    # 定时校验 access_token 是否过期，如果过期则需要获取 access_token
    async def check_accesstoken(self):
        if self.access_token_gettime == 0:
            pass

    # 获取access_token
    async def get_access_token(self, headler):
        http = httpclient.AsyncHTTPClient()
        http_get = await http.fetch(self.access_token_url.format(self.appid, self.secret, self.grant_type))
        _data = http_get.body.decode('utf-8')
        _dict_data = json.loads(_data)
        aa = CFun.filter_url(headler.get_query_argument('ccccc', ''))
        logging.info(str(_dict_data))
        logging.info(aa)

        if _dict_data["errcode"] == 0:
            pass
        headler.write(_data)

    # 登录
    async def login(self, request):
        code = CFun.filter_url(request.arguments["code"])
        anonymous_code = CFun.filter_url(request.arguments["anonymous_code"])
        pttype = CFun.filter_url(request.arguments["pttype"])
        ptid = CFun.filter_url(request.arguments["ptid"])
        channel = CFun.filter_url(request.arguments["channel"])
        devicetype = CFun.filter_url(request.arguments["devicetype"])

        http = httpclient.AsyncHTTPClient()
        http_get = await http.fetch(self.login_url.format(self.appid, self.secret, code, anonymous_code))
        _data = http_get.body.decode('utf-8')
        _dict_data = json.loads(_data)

        if _dict_data["errcode"] == 0:
            # 判断是否首次进入注册角色
            pass
        print("aa", _dict_data)
        request.write(_data)
        pass

    #登录获取数据
    def GetMsg(self, code, errmsg):
        pass
