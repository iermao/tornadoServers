# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 任务模块
# 成就模块

import json
import time

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData


class Task(object):
    def __init__(self):
        self.taskdata = {}
        self.achievvedata = {}
        self.taskobjlist = {}

    async def init(self):
        pass

    # 初始化任务数据
    async def initData(self):
        await self.inittaskdata()
        await self.sendtaskdata()

    # 保存任务数据
    async def SaveData(self):
        await self.DBM.Save_taskdata(self)

    # 发送所有任务数据
    async def sendtaskdata(self):
        _msg = {"id": MsgDefine.USER_MSG_INITTASKDATA, "data": self.taskdata}
        await self.ToClientMsg(_msg)

    # 初始化任务数据
    async def inittaskdata(self):
        for key in ConfigData.renwu_Data.keys():
            _data = TaskData()
            if (key in self.taskdata.keys()):
                await _data.init_db(self.taskdata[str(key)])
            else:
                await _data.init_new(key)
            print(key, _data.id)
            _tmpdata = await _data.To_arr()

            self.taskdata[str(_data.id)] = _tmpdata
            self.taskobjlist[_data.id] = _data

    # 做任务
    async def do_task(self, _taskid):
        pass


class TaskData():
    def __init__(self):
        self.id = 0
        self.type = 0
        self.num = 0
        self.rewardType = [0]
        self.rewardPra = 0
        self.donums = 0
        pass

    async def init_new(self, _id):
        if _id in ConfigData.renwu_Data.keys():
            self.id = _id
            self.type = ConfigData.renwu_Data[_id]["type"]
            self.num = ConfigData.renwu_Data[_id]["num"]
            self.rewardType = ConfigData.renwu_Data[_id]["rewardType"]
            self.rewardPra = eval(ConfigData.renwu_Data[_id]["rewardPra"])
            self.donums = 0

    async def init_db(self, _arr=[0, 0, 0, [0], 0, 0]):
        self.id = _arr[0]
        self.type = _arr[1]
        self.num = _arr[2]
        self.rewardType = _arr[3]
        self.rewardPra = _arr[4]
        self.donums = [5]

    async def To_arr(self):
        _data = []
        _data.append(self.id)
        _data.append(self.type)
        _data.append(self.num)
        _data.append(self.rewardType)
        _data.append(self.rewardPra)
        _data.append(self.donums)
        return _data

    async def add_donums(self):
        if (self.donums < self.id):
            self.donums += 1
        pass