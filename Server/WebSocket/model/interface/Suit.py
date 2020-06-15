# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 换装模块

import json
import time
import datetime
import copy

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData


class Suit(object):
    def __init__(self):

        # 当前穿搭数据
        self.suitdata = []

        # 当前穿搭衣服数据主题数据
        self.suitmodel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        #主题模特领取奖励状态
        self.thememodelre = {}

        # 当前衣服物品数据
        self.dressdata = []
        # 待出售的衣服临时数据
        self.soldsuit = []
        # 套装数据
        self.suitlist = {}
        # 保存的套装数据
        self.savesuit = []

        pass

    async def init(self):
        pass

    async def initData(self):
        homedata = await self.DBM.getHomeData(self.cid)
        self.suitdata = homedata["suitdata"]
        self.dressdata = homedata["dressdata"]
        self.suitlist = homedata["suitlist"]

        _savesuit = await self.DBM.getsavesuitdata(self.cid)
        self.savesuit = _savesuit["data"]

        # //计算主题数据
        await self.SetThememodelval()

        await self.Sendsuitdata()
        await self.Senddressdata()
        await self.Sendsuitlist()
        await self.Sendsavesuit()

    async def SaveData(self):
        await self.sold_moresuit()
        await self.DBM.Save_homedata(self)
        await self.DBM.Save_savesuitdata(self)

    # 当前穿搭数据
    async def Sendsuitdata(self):
        _msg = {"id": MsgDefine.USER_MSG_SUITATA, "data1": self.suitdata, "data2": self.suitmodel}
        await self.ToClientMsg(_msg)

    # 当前衣服物品数据
    async def Senddressdata(self):
        _msg = {"id": MsgDefine.USER_MSG_DRESSDATA, "data": self.dressdata}
        await self.ToClientMsg(_msg)

    # 套装数据
    async def Sendsuitlist(self):
        _msg = {"id": MsgDefine.USER_MSG_SUITLIST, "data": self.suitlist}
        await self.ToClientMsg(_msg)

    # 发送保存的套装数据
    async def Sendsavesuit(self):
        _msg = {"id": MsgDefine.USER_MSG_SAVESUITDATA, "data": self.savesuit}
        await self.ToClientMsg(_msg)

    # 保存套装数据
    async def C_savesuit(self):
        _leng = len(self.savesuit)
        _ishas = False
        # print(self.savesuit)
        # print(self.suitdata)
        for _val in self.savesuit:
            if (self.suitdata == _val):
                _ishas = True
                break
        if (_ishas):
            await self.SendToClientTips(101056)  #已经有保存的穿搭数据
            return False
        if (_leng > 4):
            await self.SendToClientTips(101055)  #保存的穿搭数据已满
            return False
        _copylist = copy.deepcopy(self.suitdata)
        self.savesuit.append(_copylist)
        _msg = {"id": 0, "data": "穿搭保存成功！"}
        await self.To_C_Tips(_msg)  #保存的穿搭数据已满
        await self.Sendsavesuit()

    # 保存时装数据操作
    async def C_savesuitaction(self, _id, _type):
        # print("C_savesuitaction", _id, _type)
        # 删除
        if (_type == 1):
            _val = copy.deepcopy(self.savesuit[_id])
            if (len(_val) > 0):
                self.savesuit.remove(_val)
                await self.Sendsavesuit()
            else:
                return False
        # 装备
        if (_type == 2):
            _val = copy.deepcopy(self.savesuit[_id])
            if (len(_val) > 0):
                self.suitdata = _val
                await self.Sendsuitdata()

    # 增加衣服数据
    async def add_suit(self, dressid, _type):

        if dressid > 1:
            # 衣服已经拥有
            if (dressid in self.dressdata):
                _data = {"id": dressid, "sta": 1, "type": _type}
                self.soldsuit.append(dressid)
            # 衣服没有
            else:
                self.dressdata.append(dressid)
                _data = {"id": dressid, "sta": 0, "type": _type}
                await self.add_suitlist(dressid)  # 套装数据

            # 衣服为种子获得
            if _type == "plant":
                # 做任务类型为1的任务【召唤衣服】
                await self.do_task_type(1)

        else:
            _data = {"id": -1, "sta": 0, "type": _type}

        _msg = {"id": MsgDefine.USER_MSG_PLANT_HARVEST, "data": _data}  # 收获弹出衣服提示
        await self.ToClientMsg(_msg)
        await self.Senddressdata()

    # 增加套装
    async def add_suitlist(self, dressid):
        _dresscon = ConfigData.dress_Data[dressid]
        if (_dresscon is None):
            return False
        _suitid = _dresscon["suitId"]
        # print("add_suitlist", self.suitlist.keys())
        if (str(_suitid) in self.suitlist.keys()):
            _vallist = self.suitlist[str(_suitid)]

            if (dressid in _vallist):
                return False
            _vallist.append(dressid)
            self.suitlist[str(_suitid)] = _vallist

            if (len(_vallist) == 9):
                await self.do_achieve_bytype(4, 1)  # 触发成就---获取套装
                await self.add_paymoney(100, "集齐套装奖励")  #集齐套装给100钻石奖励
                _suitcon = ConfigData.suit_Data[_suitid]
                _suittype = _suitcon["fame"]
                if (_suittype == 1):
                    await self.do_achieve_bytype(7, 1)  # 触发成就---收集整套C级套装
                elif (_suittype == 2):
                    await self.do_achieve_bytype(8, 1)  # 触发成就---收集整套B级套装
                elif (_suittype == 3):
                    await self.do_achieve_bytype(9, 1)  # 触发成就---收集整套A级套装
                elif (_suittype == 4):
                    await self.do_achieve_bytype(10, 1)  # 触发成就---收集整套S级套装

                # # 套装提示
                # await self.showitemtips(11, _suitid, 1, 1, 1)
        else:
            _vallist = []
            _vallist.append(dressid)
            self.suitlist[str(_suitid)] = _vallist

        # 发送套装数据
        await self.Sendsuitlist()

    # 换衣服
    async def C_Suit_Change(self, dressid):
        if (dressid in self.dressdata):
            _tmpdata = ConfigData.dress_Data[dressid]
            _partTag = int(_tmpdata['partTag'])
            self.suitdata[_partTag] = dressid
            await self.SetThememodelval()
        await self.Sendsuitdata()

    # 计算是否开始主题模特
    async def checkthememodel(self):
        pass
        # modelstarttime = {12, 13, 14, 19}
        # modeltimes = 59

        # pass

    # 计算时装模特数值
    async def SetThememodelval(self):
        _themelist = []
        for _val in self.suitdata:
            if (_val > 0):
                _tmpdata = ConfigData.dress_Data[_val]
                _tmlthemedata = _tmpdata["themeStyle"]
                if (_tmlthemedata is None or _tmlthemedata is ""):
                    continue
                _tmlthemedata
                _tmplist = str(_tmlthemedata).split(",")
                if len(_tmplist) < 2:
                    continue
                _themelist.append(int(_tmplist[0]))
                _themelist.append(int(_tmplist[1]))
                pass
            pass
        # print("_themelist", _themelist)
        self.suitmodel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for _val in _themelist:
            self.suitmodel[_val] = self.suitmodel[_val] + 1

    # 时装模特领取奖励
    async def C_thememodel_re(self, percent):

        # 声望奖励
        for _val in self.suitdata:
            if (_val > 0):
                _dressdata = ConfigData.dress_Data[_val]
                _suitid = _dressdata["suitId"]
                _suitdata = ConfigData.suit_Data[_suitid]
                _seedid = _suitdata["seedId"]
                await self.addshengwangnums(_seedid, 100)

        # 金币奖励
        if (percent < 30):
            return False
        elif (percent >= 30 and percent < 50):
            self.add_gamemoney(520)
        elif (percent >= 50 and percent < 80):
            self.add_gamemoney(840)
        elif (percent >= 80 and percent < 100):
            self.add_gamemoney(1160)
        elif (percent >= 100):
            self.add_gamemoney(1480)

        if (percent >= 100):
            await self.do_achieve_bytype(12, 1)  # 触发成就---主题模特完成数量+1

    # 出售多余的衣服
    async def C_Plant_soldsuit(self, dressid):
        _tmpdata = ConfigData.dress_Data[dressid]
        # print(dressid, _tmpdata)
        if (_tmpdata != None):
            _type = _tmpdata["sellType"]
            _money = _tmpdata["sellPrice"]
            if (_type == 1):
                _state = await self.add_gamemoney(_money)
            if (_type == 2):
                _state = await self.add_paymoney(_money)
            # 出售装备
            if dressid in self.soldsuit:
                self.soldsuit.remove(dressid)

    # 存档查看是否有没有出售的衣服
    async def sold_moresuit(self):
        if (len(self.soldsuit) > 0):
            for _id in self.soldsuit:
                await self.C_Plant_soldsuit(_id)
        self.soldsuit = []
