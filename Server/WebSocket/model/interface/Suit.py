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
        pass

    async def init(self):
        pass

    async def initData(self):
        homedata = await self.DBM.getHomeData(self.cid)
        self.suitdata = homedata["suitdata"]
        self.dressdata = homedata["dressdata"]

        await self.Sendsuitdata()
        await self.Senddressdata()

    async def SaveData(self):
        await self.DBM.Save_homedata(self)

    async def Sendsuitdata(self):
        _msg = {"id": MsgDefine.USER_MSG_SUITATA, "data": self.suitdata}
        await self.ToClientMsg(_msg)

    async def Senddressdata(self):
        _msg = {"id": MsgDefine.USER_MSG_DRESSDATA, "data": self.dressdata}
        await self.ToClientMsg(_msg)

    # 增加衣服数据
    async def add_suit(self, dressid):
        # print("add_suit", self.dressdata)
        if (dressid in self.dressdata):
            pass
        else:
            self.dressdata.append(dressid)
        await self.Senddressdata()

    # 换衣服
    async def C_Suit_Change(self, dressid):
        if (dressid in self.dressdata):
            _tmpdata = ConfigData.dress_Data[dressid]
            _partTag = int(_tmpdata['partTag'])
            self.suitdata[_partTag] = dressid
        await self.Sendsuitdata()
