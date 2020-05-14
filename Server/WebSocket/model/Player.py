import os
import json
import time

from . import ConfigData

from .interface import BaseUser
from .interface import Suit
from .interface import Farm
from .interface import Task

from . import MsgDefine


#玩家
class Player(BaseUser, Suit, Farm, Task):
    def __init__(self):
        # 玩家数据
        self.basedata = {}
        BaseUser.__init__(self)
        Suit.__init__(self)
        Farm.__init__(self)
        Task.__init__(self)
        # pass

    async def init(self, tmpuser, tmpcid, tmppwd, tmpDBM):
        print("Player  __init__")
        await BaseUser.init(self, tmpuser, tmpcid, tmpDBM)

        await Suit.init(self)
        await Farm.init(self)
        await Task.init(self)

        await self.initData()

        await Suit.initData(self)
        await Farm.initData(self)
        await Task.initData(self)
        pass
        # print(ConfigData.level_Data)
        # self.add_gamemoney(1000)
        # self.add_paymoney(100)

    # 登录获取数据
    async def initData(self):
        # 基础数据
        self.basedata = await self.DBM.getBaseData(self.cid)
        await self.Sendbasedata()

    # 登录初始化发送数据---begin
    async def Sendbasedata(self):
        _msg = {"id": MsgDefine.USER_MSG_BASEDATA, "data": self.basedata}
        await self.ToClientMsg(_msg)

    # 登录初始化发送数据---end

    # 下线保存所有数据保存数据
    async def SaveData_ALL(self):
        await BaseUser.SaveData(self)
        await Suit.SaveData(self)
        await Farm.SaveData(self)
        await Task.SaveData(self)

    async def addexp(self, _exp):
        _exp = int(_exp)
        if (_exp <= 0):
            return False
        _nowexp = self.basedata["exp"]

        _nowlvlexp = ConfigData.level_Data[self.basedata["level"]]["exp"]

        _tmpexp = _nowexp + _exp

        if (_tmpexp >= _nowlvlexp):
            await self.Leveliup(1)
            await self.addexp(_tmpexp - _nowlvlexp)
        else:
            self.basedata["exp"] += _exp

        await self.Sendbasedata()
        return True

    # 升级
    async def Leveliup(self, _addlevel):
        _addlevel = int(_addlevel)
        if (_addlevel < 1):
            return False
        self.basedata["level"] += _addlevel
        self.basedata["exp"] = 0
        return True

    #获取游戏币
    async def get_gamemoney(self):
        return int(self.basedata["gamemoney"])

    # 增加货币
    async def add_gamemoney(self, _value):
        _value = int(_value)
        if (_value <= 0):
            return False
        self.basedata["gamemoney"] += _value

        await self.Sendbasedata()
        return True

    # 减少货币
    async def rec_gamemoney(self, _value):
        _value = int(_value)
        if (_value <= 0):
            return False
        _nowmoney = await self.get_gamemoney()
        if (_nowmoney < _value):
            return False
        self.basedata["gamemoney"] -= _value

        await self.Sendbasedata()
        return True

    # 获取钻石
    async def get_paymoney(self):
        return int(self.basedata["paymoney"])

    # 增加钻石
    async def add_paymoney(self, _value):
        _value = int(_value)
        if (_value <= 0):
            return False
        self.basedata["paymoney"] += _value

        await self.Sendbasedata()
        return True

    # 钻石减少
    async def rec_paymoney(self, _value):
        _value = int(_value)
        if (_value <= 0):
            return False
        _nowval = await self.get_paymoney()
        if (_nowval < _value):
            return False
        self.basedata["paymoney"] -= _value

        await self.Sendbasedata()
        return True
