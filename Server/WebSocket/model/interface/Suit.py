# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 换装模块

import json
import time

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData


class Suit(object):
    def __init__(self):

        # 当前穿搭数据
        self.suitdata = []
        # 当前衣服物品数据
        self.dressdata = []
        # 待出售的衣服临时数据
        self.soldsuit = []
        # 套装数据
        self.suitlist = {}

        pass

    async def init(self):
        pass

    async def initData(self):
        homedata = await self.DBM.getHomeData(self.cid)
        self.suitdata = homedata["suitdata"]
        self.dressdata = homedata["dressdata"]
        self.suitlist = homedata["suitlist"]

        await self.Sendsuitdata()
        await self.Senddressdata()
        await self.Sendsuitlist()

    async def SaveData(self):
        await self.sold_moresuit()
        await self.DBM.Save_homedata(self)

    # 当前穿搭数据
    async def Sendsuitdata(self):
        _msg = {"id": MsgDefine.USER_MSG_SUITATA, "data": self.suitdata}
        await self.ToClientMsg(_msg)

    # 当前衣服物品数据
    async def Senddressdata(self):
        _msg = {"id": MsgDefine.USER_MSG_DRESSDATA, "data": self.dressdata}
        await self.ToClientMsg(_msg)

    # 套装数据
    async def Sendsuitlist(self):
        _msg = {"id": MsgDefine.USER_MSG_SUITLIST, "data": self.suitlist}
        await self.ToClientMsg(_msg)

    # 增加衣服数据
    async def add_suit(self, dressid):

        # 衣服已经拥有
        if (dressid in self.dressdata):
            _data = {"id": dressid, "sta": 1}
            self.soldsuit.append(dressid)
        # 衣服没有
        else:
            self.dressdata.append(dressid)
            _data = {"id": dressid, "sta": 0}
            await self.add_suitlist(dressid)  # 套装数据

        _msg = {"id": MsgDefine.USER_MSG_PLANT_HARVEST, "data": _data}  # 收获弹出衣服提示
        await self.ToClientMsg(_msg)
        await self.Senddressdata()
        # 做任务类型为1的任务【召唤衣服】
        await self.do_task_type(1)

    # 增加套装
    async def add_suitlist(self, dressid):
        _dresscon = ConfigData.dress_Data[dressid]
        if (_dresscon is None):
            return False
        _suitid = _dresscon["suitId"]
        print("add_suitlist", self.suitlist.keys())
        if (str(_suitid) in self.suitlist.keys()):
            _vallist = self.suitlist[str(_suitid)]

            if (dressid in _vallist):
                return False
            _vallist.append(dressid)
            self.suitlist[str(_suitid)] = _vallist
        else:
            _vallist = []
            _vallist.append(dressid)
            self.suitlist[str(_suitid)] = _vallist

    # 换衣服
    async def C_Suit_Change(self, dressid):
        if (dressid in self.dressdata):
            _tmpdata = ConfigData.dress_Data[dressid]
            _partTag = int(_tmpdata['partTag'])
            self.suitdata[_partTag] = dressid
        await self.Sendsuitdata()

    # 出售多余的衣服
    async def C_Plant_soldsuit(self, dressid):
        _tmpdata = ConfigData.dress_Data[dressid]
        if (_tmpdata != None):
            _type = _tmpdata["sellType"]
            _money = _tmpdata["sellPrice"]
            if (_type == 1):
                _state = await self.add_gamemoney(_money)
            if (_type == 2):
                _state = await self.add_paymoney(_money)
            self.soldsuit.remove(dressid)

    # 存档查看是否有没有出售的衣服
    async def sold_moresuit(self):
        if (len(self.soldsuit) > 0):
            for _id in self.soldsuit:
                await self.C_Plant_soldsuit(_id)
        self.soldsuit = []
