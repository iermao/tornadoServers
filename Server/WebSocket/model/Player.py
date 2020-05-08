import os
import json
import datetime
import time

from .pUser import BaseUser
from .SuitData import SuitData


#玩家
class Player(BaseUser, SuitData):
    # 创建时间
    nCreatetime = time.time()
    # 登录时间
    nLogintime = time.time()
    # 登出时间
    nLlogouttime = time.time()
    #等级
    nLelve = 1
    # 游戏币
    nGamemoney = 0
    # 充值货币
    nPaymoney = 1
    # 当前等级经验
    nExp = 0

    def __init__(self, _user, cid, _pwd, DB):
        print("Player  __init__")
        BaseUser.__init__(self, _user, cid, DB)
        SuitData.__init__(self)
        # print(self.cid)

    def GetData(self):
        udata = self.DB.getPlayData()
        pass

    def getusermsg(self):
        pass

    # 升级
    def Leveliup(self, _addlevel):
        self.nLelve += _addlevel

    def UpdateGameMoney(self, _money):
        if (_money < 0):
            if (_money > self.nGamemoney):
                pass
        elif (_money > 0):
            pass
