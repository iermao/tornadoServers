import os
import json
import datetime
import time

from .pUser import BaseUser
from .SuitData import SuitData

from . import MsgDefine


#玩家
class Player(BaseUser, SuitData):
    # 创建时间
    nCreatetime = time.time()
    # 登录时间
    nLogintime = time.time()
    # 登出时间
    nLlogouttime = time.time()

    # 玩家数据
    basedata = {}
    # 当前穿搭数据
    suitdata = []
    # 当前衣服物品数据
    dressdata = []

    # 初始化植物数据
    plantdata = {}
    # 初始化种子数据
    seeddata = {}

    def __init__(self, _user, cid, _pwd, _DBM):
        print("Player  __init__")
        BaseUser.__init__(self, _user, cid, _DBM)
        SuitData.__init__(self)
        self.GetData()

    def GetData(self):
        # 基础数据
        self.basedata = self.DBM.getBaseData(self.cid)
        self.suitdata = self.DBM.getHomeData(self.cid)["suitdata"]
        self.dressdata = self.DBM.getHomeData(self.cid)["dressdata"]
        self.plantdata = self.DBM.getSeedAndPlantData(self.cid)["plantdata"]
        self.seeddata = self.DBM.getSeedAndPlantData(self.cid)["seeddata"]

        self.Sendbasedata()
        self.Sendsuitdata()
        self.Senddressdata()
        self.Sendplantdata()
        self.Sendseeddata()

    def Sendbasedata(self):
        _msg = {"id": MsgDefine.USER_MSG_BASEDATA, "data": self.basedata}
        self.pobj.write_message(_msg)

    def Sendsuitdata(self):
        _msg = {"id": MsgDefine.USER_MSG_SUITATA, "data": self.suitdata}
        self.pobj.write_message(_msg)

    def Senddressdata(self):
        _msg = {"id": MsgDefine.USER_MSG_DRESSDATA, "data": self.dressdata}
        self.pobj.write_message(_msg)

    def Sendplantdata(self):
        _msg = {"id": MsgDefine.USER_MSG_PLANTDATA, "data": self.plantdata}
        self.pobj.write_message(_msg)

    def Sendseeddata(self):
        _msg = {"id": MsgDefine.USER_MSG_SEEDDATA, "data": self.seeddata}
        self.pobj.write_message(_msg)

    def SaveData(self):
        self.DBM.Save_BaseData(self)
        self.DBM.Save_homedata(self)
        self.DBM.Save_farmdata(self)

    # 升级
    def Leveliup(self, _addlevel):
        self.nLelve += _addlevel

    def UpdateGameMoney(self, _money):
        if (_money < 0):
            if (_money > self.nGamemoney):
                pass
        elif (_money > 0):
            pass
