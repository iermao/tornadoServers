# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 玩家基础模块

import json
import time

from Server.WebSocket.model import MsgDefine


# 用户基础对象
class BaseUser(object):
    def __init__(self):
        pass

    async def init(self, _user, cid, _DBM):
        self.cid = cid
        self.pobj = _user
        self.logintime = time.time() * 1000
        self.logouttime = time.time() * 1000
        self.DBM = _DBM

        # 初始化数据
        await self.initData()

    async def close(self):
        self.logouttime = time.time() * 1000

    #初始化部分数据
    async def initData(self):
        # 初始化玩家数据
        await self.DBM.initplayerdata(self.cid)

    async def SaveData(self):
        await self.DBM.Save_BaseData(self)

    # 接受消息
    async def ClientToServer(self, msg):
        # print(str(msg))
        try:
            _msg = json.loads(msg)
        except:
            print("json 解析报错！")
            return
        _msgid = int(_msg["id"])
        # print("ClientToServer__",_msgid,type(_msg["data"]),_msg["data"])

        if (_msgid == MsgDefine.USER_MSG_BUYSEED):  # 购买种子
            await self.client_buyseed(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT):  # 种植
            await self.client_plantnew(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_PICK):  # 植物状态按钮点击
            await self.client_plantpick(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_CHECK):  # 植物状态检测
            await self.client_plantcheckstate(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_CHANGESUIT):  # 植物状态检测
            await self.client_chengesuit(_msg["data"])

        elif (False):
            pass
        else:
            pass

    # 给客户端发送消息
    async def ToClientMsg(self, msg):
        # print(msg)
        _msg = json.dumps(msg)
        # print(_msg)
        self.pobj.write_message(_msg)

    # **********************************************************
    # 客户端消息处理
    # **********************************************************
    # 买种子
    async def client_buyseed(self, msg):
        _seedid = msg['seedid']
        _count = msg["count"]
        await self.C_buy_seed(_seedid, _count)

    # 种植土地
    async def client_plantnew(self, msg):
        index = int(msg['index'])
        seedid = msg["seedid"]
        await self.C_Plant_seed(index, seedid)

    # 土地状态点击
    async def client_plantpick(self, msg):
        index = int(msg['index'])
        await self.C_Plant_pick(index)

    # 检测土地状态
    async def client_plantcheckstate(self, msg):
        index = int(msg['index'])
        await self.C_Plant_check(index)

    #换装
    async def client_chengesuit(self, msg):
        _id = int(msg['id'])
        await self.C_Suit_Change(_id)
