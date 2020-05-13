import json
import time

from Server.WebSocket.model import MsgDefine


class Suit(object):
    def __init__(self):
        # 当前穿搭数据
        self.suitdata = []
        # 当前衣服物品数据
        self.dressdata = []
        pass

    async def init(self):
        pass

    async def Sendsuitdata(self):
        _msg = {"id": MsgDefine.USER_MSG_SUITATA, "data": self.suitdata}
        await self.ToClientMsg(_msg)

    async def Senddressdata(self):
        _msg = {"id": MsgDefine.USER_MSG_DRESSDATA, "data": self.dressdata}
        await self.ToClientMsg(_msg)
