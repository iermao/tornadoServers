
import json
import time

from Server.WebSocket.model import MsgDefine

# 用户基础对象
class BaseUser(object):

    def __init__(self, _user, cid, _DBM):
        print("User  __init__")
        self.cid = cid
        self.pobj = _user
        self.logintime = time.time()*1000
        self.logouttime = time.time()*1000
        self.DBM = _DBM

        # 初始化数据
        self.initData()
    def close(self):
        self.logouttime = time.time()*1000
    #初始化部分数据
    def initData(self):
        # 初始化玩家数据
        self.DBM.initplayerdata(self.cid)

    def ToClientMsg(self, msg):
        pass