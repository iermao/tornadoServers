# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 玩家模块 ----会继承其他几个模块

import os
import json
import time

from Server.WebSocket.model import Fun

from . import ConfigData

from .interface import BaseUser
from .interface import Suit
from .interface import Farm
from .interface import Task

from . import MsgDefine


#玩家
class Player(BaseUser, Suit, Farm, Task):
    def __init__(self):
        self.herttime = time.time()
        # 玩家数据

        self.basedata = {}
        self.newday = False
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

        if (self.newday):
            await self.NewDay()

    # 登录获取数据
    async def initData(self):
        # 基础数据
        self.basedata = await self.DBM.getBaseData(self.cid)

        # 获取上次登录时间
        _lastlogintime = self.basedata["logintime"] / 1000
        _nowlogintime = time.time()
        _days = Fun.get_delta_days(_lastlogintime, _nowlogintime)
        # 新的一天
        if (_days > 0):
            self.newday = True

        await self.Sendbasedata()

    # 新的一滩需要重置的数据
    async def NewDay(self):
        self.newday = True
        self.basedata["dayonline"] = 0
        await self.Sendbasedata()
        self.dayonlinerew = []
        await self.sendonlinerewdata()

    # 登录初始化发送数据---begin
    async def Sendbasedata(self):
        _msg = {"id": MsgDefine.USER_MSG_BASEDATA, "data": self.basedata}
        await self.ToClientMsg(_msg)

    # 登录初始化发送数据---end

    # 下线保存所有数据保存数据
    async def SaveData_ALL(self):
        await Suit.SaveData(self)
        await Farm.SaveData(self)
        await Task.SaveData(self)

        # 最后在保存玩家数据
        await BaseUser.SaveData(self)

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

        _msg = {"id": 0, "data": "获得经验x" + str(_exp)}
        await self.To_C_Tips(_msg)

        # await self.Sendbasedata()
        await self.SendBasedata_bykey("exp", self.basedata["exp"])
        return True

    # 升级
    async def Leveliup(self, _addlevel):
        _addlevel = int(_addlevel)
        if (_addlevel < 1):
            return False

        self.basedata["level"] += _addlevel
        self.basedata["exp"] = 0
        await self.SendBasedata_bykey("level", self.basedata["level"])

        await self.do_achieve_bytype(1, self.basedata["level"])  # # 触发成就---升级

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
        _msg = {"id": 0, "data": "获得金币x" + str(_value)}
        await self.To_C_Tips(_msg)
        # await self.Sendbasedata()
        await self.SendBasedata_bykey("gamemoney", self.basedata["gamemoney"])
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
        # await self.Sendbasedata()
        await self.SendBasedata_bykey("gamemoney", self.basedata["gamemoney"])
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
        _msg = {"id": 0, "data": "获得钻石x" + str(_value)}
        await self.To_C_Tips(_msg)
        # await self.Sendbasedata()
        await self.SendBasedata_bykey("paymoney", self.basedata["paymoney"])
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
        # await self.Sendbasedata()
        await self.SendBasedata_bykey("paymoney", self.basedata["paymoney"])
        return True

    # 幸运抽奖开始
    async def C_Lucky_start(self, _type):
        if (_type == 2):
            await self.rec_paymoney(10)
        self.basedata["lucktime"] = time.time() * 1000
        return True

    # 幸运抽奖奖励
    async def C_Lucky_reward(self, _luckyid, _itemid):
        _con_data = ConfigData.lucky_Data[_luckyid]
        if (_con_data != None):
            _rewardType = _con_data['rewardType']
            _rewardPra = eval(_con_data['rewardPra'])

            # 做任务类型为3的任务【摇奖】
            await self.do_task_type(4)

            if (_rewardType == 1):  # 奖励金币
                _count = _rewardPra[0]
                await self.add_gamemoney(_count)
            elif (_rewardType == 2):  # 奖励钻石
                _count = _rewardPra[0]
                await self.add_paymoney(_count)
            elif (_rewardType == 5):  # 奖励种子
                if (_itemid not in _rewardPra):
                    return False
                _seedid = _itemid
                _count = _rewardPra[2]
                await self.Add_seed(_seedid, _count)  # 增加种子
