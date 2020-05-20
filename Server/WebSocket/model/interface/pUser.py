# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 玩家基础模块

import json
import time
from tornado import gen

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData


# 用户基础对象
class BaseUser(object):
    def __init__(self):
        pass

    async def init(self, _user, cid, _DBM):
        self.cid = cid
        self.pobj = _user
        self.logintime = time.time() * 1000
        self.logouttime = time.time() * 1000
        self.foronlinetime = time.time() * 1000  # 计算在下时间用的
        self.DBM = _DBM
        # 初始化数据
        await self.initInsertData()

        self.savetime = time.time()

    async def timersavedata(self):
        self.savetime = time.time()
        await self.SaveData_ALL()

    async def close(self):
        self.logouttime = time.time() * 1000

    #初始化部分数据
    async def initInsertData(self):
        # 初始化玩家数据
        await self.DBM.initplayerdata(self.cid)

    async def SaveData(self):

        # 本次在线时间
        _online = (time.time() - self.foronlinetime / 1000) / 60
        self.basedata["allonline"] = self.basedata["allonline"] + _online
        self.basedata["dayonline"] = self.basedata["dayonline"] + _online
        self.foronlinetime = time.time() * 1000  # 计算在下时间用的

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
        if (_msgid == MsgDefine.MSG_HERTMSG):  # 心跳数据
            await self.client_Hertbeat()

        elif (_msgid == MsgDefine.USER_MSG_BUYSEED):  # 购买种子
            await self.client_buyseed(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT):  # 种植
            await self.client_plantnew(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_PICK):  # 植物状态按钮点击
            await self.client_plantpick(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_CHECK):  # 植物状态检测
            await self.client_plantcheckstate(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_CHANGESUIT):  # 植物状态检测
            await self.client_changesuit(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_NEW):  # 开垦一个新的土地
            await self.client_newland(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_HARVEST):  # 收获植物
            await self.client_harvest(_msg["data"])
        elif (_msgid == MsgDefine.USER_MSG_PLANT_SOLDSUIT):
            await self.client_soldsuit(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_TASKREWARD):  # 任务领取
            await self.client_taskreward(_msg["data"])

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

    async def SendToClientTips(self, id):
        _mgstr = ConfigData.GetMsgstr(id)
        _msg = {"id": id, "data": _mgstr}
        await self.To_C_Tips(_msg)

    async def To_C_Tips(self, msg):
        _msg = {"id": MsgDefine.GAME_MSG_TIPSMSG, "data": msg}
        await self.ToClientMsg(_msg)

    # **********************************************************
    # 客户端消息处理
    # **********************************************************

    # 心跳数据
    async def client_Hertbeat(self):
        print("client_Hertbeat")
        _times = time.time()
        if ((_times - self.savetime) / 60.0 >= 5):
            await self.timersavedata()

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
    async def client_changesuit(self, msg):
        _id = int(msg['id'])
        await self.C_Suit_Change(_id)

    #开垦新的土地
    async def client_newland(self, msg):
        _id = int(msg['id'])
        await self.C_New_Plant(_id)

    # 收获
    async def client_harvest(self, msg):
        _id = int(msg['index'])
        _type = int(msg['type'])
        await self.C_Plant_Havest(_id, _type)

    # 出售衣服
    async def client_soldsuit(self, msg):
        _id = int(msg['id'])
        await self.C_Plant_soldsuit(_id)

    # 任务领取奖励
    async def client_taskreward(self, msg):
        _id = int(msg['id'])
        await self.C_task_reward(_id)
