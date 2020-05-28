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

        # 任务数据
        self.taskdata = {}
        self.taskobjlist = {}

        # 成就数据
        self.achievedata = {}
        self.achieveobjlist = {}

        # 在线奖励数据
        self.dayonlinerew = []

        #玩家开放场景数据
        self.openscene = []

    async def init(self):
        pass

    # 初始化任务数据
    async def initData(self):
        _taskdata = await self.DBM.gettaskdata(self.cid)
        self.taskdata = _taskdata["data"]
        self.dayonlinerew = _taskdata["dayonlinerew"]
        self.openscene = _taskdata["openscene"]

        _achievedata = await self.DBM.getachievedata(self.cid)
        self.achievedata = _achievedata["data"]

        # 新的一天
        if (self.newday):
            self.taskdata = {}

        # 初始化任务数据
        await self.inittaskdata()
        # 初始化成就数据
        await self.initachievedata()

        await self.sendtaskdata()

        await self.sendonlinerewdata()

        await self.sendopenscenedata()

        await self.sendachievedata()

    # 保存数据
    async def SaveData(self):
        await self.DBM.Save_taskdata(self)
        await self.DBM.Save_achievedata(self)

    # 发送所有任务数据
    async def sendtaskdata(self):
        _msg = {"id": MsgDefine.USER_MSG_INITTASKDATA, "data": self.taskdata}
        await self.ToClientMsg(_msg)

    # 初始化发送在线奖励数据
    async def sendonlinerewdata(self):
        _msg = {"id": MsgDefine.USER_MSG_ONLINEREWARDINIT, "data": self.dayonlinerew}
        await self.ToClientMsg(_msg)

    # 初始化发送开放场景数据
    async def sendopenscenedata(self):
        _msg = {"id": MsgDefine.USER_MSG_OPENSCENEDATA, "data": self.openscene}
        await self.ToClientMsg(_msg)

    # 初始化任务数据
    async def inittaskdata(self):
        for key in ConfigData.renwu_Data.keys():
            _data = TaskData()
            # print(self.taskdata)
            if (str(key) in self.taskdata.keys()):
                await _data.init_db(self.taskdata[str(key)])
            else:
                await _data.init_new(key)
            # print(key, _data.id)
            _tmpdata = await _data.To_arr()
            self.taskdata[str(_data.id)] = _tmpdata
            self.taskobjlist[_data.id] = _data

    # 任务对象转换为json
    async def taskobjlisttodata(self):
        for _key in self.taskobjlist.keys():
            self.taskdata[str(_key)] = await self.taskobjlist[_key].To_arr()

    # 成就对象转换为josn
    async def achieveobjlisttodata(self):
        for _key in self.achieveobjlist.keys():
            self.achievedata[str(_key)] = await self.achieveobjlist[_key].To_arr()
        # print("achievedata", self.achievedata)

    # 做任务----根据任务类型
    async def do_task_type(self, tasktype):
        for _val in self.taskobjlist.values():
            if _val.type == tasktype:
                await self.do_task_id(_val.id)

    # 做任务----根据任务id
    async def do_task_id(self, _taskid):
        _taskpbj = self.taskobjlist[_taskid]
        if (_taskpbj != None):
            _state = await _taskpbj.add_donums()
            await self.taskobjlisttodata()
            # 成功做任务了发送任务数据
            if (_state):
                await self.sendtaskdata()

    # 任务领取奖励
    async def C_task_reward(self, _taskid):
        _taskpbj = self.taskobjlist[_taskid]
        if (_taskpbj != None):
            _state = await _taskpbj.reward()
            await self.taskobjlisttodata()
            # 成功做任务了发送任务数据
            if (_state):
                _reward_type = _taskpbj.rewardType
                _reward_nums = _taskpbj.rewardPra[0]
                if (_reward_type == 1):
                    await self.add_gamemoney(_reward_nums)
                if (_reward_type == 2):
                    await self.add_paymoney(_reward_nums)
                await self.sendtaskdata()

    #在线领取奖励
    async def C_online_reward(self, _onlineid, _itemid):
        if (_onlineid not in self.dayonlinerew):
            _con_data = ConfigData.onLine_Data[_onlineid]
            if (_con_data != None):
                _rewardType = _con_data['rewardType']
                _rewardPra = eval(_con_data['rewardPra'])
                _time = _con_data['time']
                if (_time < self.basedata["dayonline"]):
                    return False
                # pass
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
                elif (_rewardType == 7):  # 奖励衣服
                    if (_itemid not in _rewardPra):
                        return False
                    _suitid = _itemid
                    await self.add_suit(_suitid)  # 增加衣服
                    await self.sold_moresuit()  # 出售多余的衣服

                self.dayonlinerew.append(_onlineid)
                await self.sendonlinerewdata()

    # 开放场景
    async def C_openscene(self, _id):
        if (_id not in self.openscene):
            _con_data = ConfigData.sceneSel_Data[_id]
            if (_con_data != None):
                unlockType = _con_data["unlockType"]
                unlockNum = _con_data["unlockNum"]
                _state = False
                if (unlockType == 1):
                    _state = await self.rec_gamemoney(unlockNum)
                elif (unlockType == 2):
                    _state = await self.rec_paymoney(unlockNum)
                if (_state):
                    self.openscene.append(_id)
                await self.sendopenscenedata()

    # --------------------------------
    # -----------------成就数据相关
    # --------------------------------

    # 发送所有成就数据
    async def sendachievedata(self):
        _msg = {"id": MsgDefine.USER_MSG_INITACHIEVEDATA, "data": self.achievedata}
        await self.ToClientMsg(_msg)

    # # 初始化成就数据
    async def initachievedata(self):
        for key in ConfigData.achive_Data.keys():
            _data = AchieveData()
            if (str(key) in self.achievedata.keys()):
                await _data.init_db(self.achievedata[str(key)])
            else:
                await _data.init_new(key)
            _tmpdata = await _data.To_arr()
            # print("initachievedata", _tmpdata)
            self.achievedata[str(_data.id)] = _tmpdata
            self.achieveobjlist[_data.id] = _data

    # 根据成就类型做成就
    async def do_achieve_bytype(self, _type, _data):
        for _val in ConfigData.achive_Data.values():
            if (_val["achievetype"] == _type):
                await self.do_achieve(_type, _val["id"], _data)

    # 做成就
    async def do_achieve(self, _type, _id, _data):
        # print("do_achieve ", _id)
        _state = False
        if _id in self.achieveobjlist.keys():
            _objval = self.achieveobjlist[_id]
            _state = True
            if (_type == 1):
                await _objval.set_donums(_data)
            else:
                await _objval.add_donums()
        if _state:
            await self.achieveobjlisttodata()
            await self.sendachievedata()

    # 成就领取奖励
    async def C_achieve_award(self, _id):
        _state = False
        if _id in self.achieveobjlist.keys():
            _objval = self.achieveobjlist[_id]
            _state = await _objval.set_rewardstate()

        if (_state):
            # 发送奖励...
            await self.achieveobjlisttodata()
            await self.sendachievedata()


# 任务数据实体类**********************************************************************************************************
class TaskData():
    def __init__(self):
        self.id = 0
        self.type = 0
        self.num = 0
        self.rewardType = 0
        self.rewardPra = [0]
        self.donums = 0
        self.rewardstate = 0

    async def init_new(self, _id):
        if _id in ConfigData.renwu_Data.keys():
            _data = ConfigData.renwu_Data[_id]
            self.id = _id
            self.type = _data["type"]
            self.num = _data["num"]
            self.rewardType = _data["rewardType"]
            self.rewardPra = eval(_data["rewardPra"])
            self.donums = 0
            self.rewardstate = 0

    async def init_db(self, _arr):
        self.id = _arr[0]
        self.type = _arr[1]
        self.num = _arr[2]
        self.rewardType = _arr[3]
        self.rewardPra = _arr[4]
        self.donums = _arr[5]
        self.rewardstate = _arr[6]

    async def To_arr(self):
        _data = []
        _data.append(self.id)
        _data.append(self.type)
        _data.append(self.num)
        _data.append(self.rewardType)
        _data.append(self.rewardPra)
        _data.append(self.donums)
        _data.append(self.rewardstate)
        return _data

    async def add_donums(self):
        if (self.donums < self.num):
            self.donums += 1
            return True
        return False

    async def reward(self):
        if (self.rewardstate == 0):
            self.rewardstate = 1
            return True
        return False


# 成就数据数据实体类
class AchieveData():
    def __init__(self):
        self.id = 0
        self.achievetype = 0
        self.achievenumber = 0
        self.rewardJb = 0
        self.rewardGems = 0
        self.donums = 0
        self.rewardstate = 0
        pass

    async def init_new(self, _id):
        if _id in ConfigData.achive_Data.keys():
            _data = ConfigData.achive_Data[_id]
            self.id = _id
            self.achievetype = _data["achievetype"]
            self.achievenumber = _data["achievenumber"]
            self.rewardJb = _data["rewardJb"]
            self.rewardGems = _data["rewardGems"]
            self.donums = 0
            self.rewardstate = 0

    async def init_db(self, _arr):
        self.id = _arr[0]
        self.achievetype = _arr[1]
        self.achievenumber = _arr[2]
        self.rewardJb = _arr[3]
        self.rewardGems = _arr[4]
        self.donums = _arr[5]
        self.rewardstate = _arr[6]

    async def To_arr(self):
        _data = []
        _data.append(self.id)
        _data.append(self.achievetype)
        _data.append(self.achievenumber)
        _data.append(self.rewardJb)
        _data.append(self.rewardGems)
        _data.append(self.donums)
        _data.append(self.rewardstate)
        return _data

    async def add_donums(self):
        if (self.donums < self.achievenumber):
            self.donums += 1
        pass

    async def set_donums(self, _val):
        # if (self.donums <= self.achievenumber):
        self.donums = _val

    async def set_rewardstate(self):
        if (self.rewardstate == 0):
            self.rewardstate = 1
            return True
        else:
            return False
