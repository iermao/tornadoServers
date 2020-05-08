
import json
import time


# 用户基础对象
class BaseUser(object):
    def __init__(self, _user, cid, _DB):
        print("User  __init__")
        self.cid = cid
        self.pNetUser = _user
        self.logintimes = time.time()
        self.DB = _DB

        # 初始化数据
        self.initData()

    #初始化部分数据
    def initData(self):
        # 初始化玩家数据
        self.DB.initplayerdata(self.cid)

    def ToClientMsg(self, msg):
        pass