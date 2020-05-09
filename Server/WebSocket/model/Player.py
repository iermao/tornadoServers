import os
import json
import datetime
import time

from .pUser import BaseUser
from .SuitData import SuitData

from . import MsgDefine


#玩家
class Player(BaseUser, SuitData):

    # 玩家数据
    basedata = {}

    # 初始化植物数据
    plantdata = {}
    # 初始化种子数据
    seeddata = {}

    def __init__(self, _user, cid, _pwd, _DBM):
        print("Player  __init__")
        BaseUser.__init__(self, _user, cid, _DBM)
        SuitData.__init__(self)
        self.GetData()

    # 登录获取数据
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

    # 登录初始化发送数据---begin
    def Sendbasedata(self):
        _msg = {"id": MsgDefine.USER_MSG_BASEDATA, "data": self.basedata}
        self.pobj.write_message(_msg)

    def Sendplantdata(self):
        _msg = {"id": MsgDefine.USER_MSG_PLANTDATA, "data": self.plantdata}
        self.pobj.write_message(_msg)

    def Sendseeddata(self):
        _msg = {"id": MsgDefine.USER_MSG_SEEDDATA, "data": self.seeddata}
        self.pobj.write_message(_msg)

    # 登录初始化发送数据---end

    # 保存数据
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
