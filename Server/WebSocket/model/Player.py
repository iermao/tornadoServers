# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 玩家模块 ----会继承其他几个模块

import os
import json
import time
import random
# import datetime

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

        # 玩家基础数据
        self.basedata = {}
        # 是否是新的一天
        self.newday = False
        # 签到数据
        self.signdata = {}
        #限时种子以及免费种子购买数据
        self.timeseeddata = {}

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

        # 限时种子购买数据设置并发送数据
        await self.set_timeseeddata()

    # 登录获取数据
    async def initData(self):
        # 基础数据
        self.basedata = await self.DBM.getBaseData(self.cid)
        # print(self.basedata)
        # 签到数据
        _signdata = await self.DBM.getsigndata(self.cid)
        self.signdata = _signdata["signdata"]

        #限时种子购买数据
        _timeseeddata = await self.DBM.get_freeseeddata(self.cid)
        self.timeseeddata = _timeseeddata["timeseeddata"]

        # 获取上次登录时间
        _lastlogintime = self.basedata["logintime"] / 1000
        _nowlogintime = time.time()
        _days = Fun.get_delta_days(_lastlogintime, _nowlogintime)
        # 新的一天
        if (_days > 0):
            self.newday = True

        # 基础数据
        await self.Sendbasedata()

        # 发送在线奖励数据
        await self.sendonlinerewdata()

        # 检测签到数据
        await self.checkSign()

    # 新的一天需要重置的数据
    async def NewDay(self):
        # 重置在线数据
        self.basedata["dayonline"] = 0
        # 发送基础数据
        await self.Sendbasedata()
        # 重置在线奖励数据
        self.dayonlinerew = []
        # 发送在线奖励数据
        await self.sendonlinerewdata()
        # 新的一天重置限时种子数据
        self.timeseeddata = {}

    # 登录初始化发送数据---begin
    async def Sendbasedata(self):
        _msg = {"id": MsgDefine.USER_MSG_BASEDATA, "data": self.basedata}
        await self.ToClientMsg(_msg)

    # 发送限时种子购买数据
    async def send_timeseeddata(self):
        _msg = {"id": MsgDefine.USER_TIMESEED, "data": self.timeseeddata}
        await self.ToClientMsg(_msg)

    # 登录初始化发送数据---end

    # 下线保存所有数据保存数据
    async def SaveData_ALL(self):
        await Suit.SaveData(self)
        await Farm.SaveData(self)
        await Task.SaveData(self)

        # 最后在保存玩家数据
        await BaseUser.SaveData(self)

    # 获取新手引导数据
    async def get_guide(self):
        return self.basedata["guidesta"]

    # 设置新手引导数据
    async def set_guide(self):
        if (self.basedata["guidesta"] == 1):
            return False
        self.basedata["guidesta"] = 1
        await self.add_gamemoney(100)
        await self.add_paymoney(20)

    # 发送签到数据
    async def sendSignData(self):
        _msg = {"id": MsgDefine.USER_MSG_SIGN, "data": self.signdata}
        await self.ToClientMsg(_msg)

    # 签到数据
    async def checkSign(self):
        if (len(self.signdata) == 0):
            self.signdata["nums"] = 0
            self.signdata["times"] = 0
            # 发送签到数据
            await self.sendSignData()
            return True
        else:
            times = self.signdata["times"]
            nums = self.signdata["nums"]
            if (times == 0):
                await self.sendSignData()
                return True
            _days = Fun.get_delta_days(times, time.time())
            # print("_days", _days, self.signdata)
            if (_days > 1 or nums > 6):
                self.signdata["nums"] = 0
                self.signdata["times"] = 0
                await self.sendSignData()
                return True
            elif _days == 1 and nums < 7:
                await self.sendSignData()
                return True

    # 客户端签到
    async def C_Sign(self):

        times = self.signdata["times"]
        _state = False
        if times == 0:
            self.signdata["times"] = time.time()
            self.signdata["nums"] = self.signdata["nums"] + 1
            _state = True
        elif times > 0:
            _days = Fun.get_delta_days(times, time.time())
            if _days == 1:
                self.signdata["times"] = time.time()
                self.signdata["nums"] = self.signdata["nums"] + 1
                _state = True
            pass
        if _state:
            nums = self.signdata["nums"]
            print("C_Sign", nums)
            await self.signgift(nums)

    # 签到奖励
    async def signgift(self, _index):
        _data = ConfigData.sign_Data[_index]
        if (_data is None):
            return False
        rewardType = _data["rewardType"]
        rewardPra = eval(_data["rewardPra"])
        # 签到领取奖励
        await self.AddItem(rewardType, rewardPra, 1, 3)

    # 增加经验数据
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

        # 升级提示
        _msg = {"id": 0, "data": "恭喜你升到了 " + str(self.basedata["level"]) + " 级", "sound": 2}
        await self.To_C_Tips(_msg)

        # 升级奖励
        _data = ConfigData.level_Data[self.basedata["level"]]
        rewardType = _data["rewardType"]
        rewardPra = eval(_data["rewardPra"])
        await self.AddItem(rewardType, rewardPra, 1, 2)

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
        _msg = {"id": 0, "data": "获得金币x" + str(_value), "sound": 1}
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
    async def add_paymoney(self, _value, _info=""):
        _value = int(_value)
        if (_value <= 0):
            return False
        self.basedata["paymoney"] += _value
        if (_info == ""):
            _msg = {"id": 0, "data": "获得钻石x" + str(_value), "sound": 1}
        else:
            _msg = {"id": 0, "data": _info + "钻石x" + str(_value), "sound": 1}
        await self.To_C_Tips(_msg)
        # await self.Sendbasedata()
        await self.SendBasedata_bykey("paymoney", self.basedata["paymoney"])
        return True

    # 钻石减少
    async def rec_paymoney(self, _value):
        _value = int(_value)
        if (_value < 0):
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
    async def C_Lucky_reward(self, _luckyid):
        _con_data = ConfigData.lucky_Data[_luckyid]
        if (_con_data != None):
            _rewardType = _con_data['rewardType']
            _rewardPra = eval(_con_data['rewardPra'])
            await self.AddItem(_rewardType, _rewardPra, 1, 1)

            # 做任务类型为4的任务【幸运摇奖】
            await self.do_task_type(4)

    # 客户端显示获得物品提示
    async def showitemtips(self, _type, _itemid, _count, _showstate, _showtype):
        _data = [_type, _itemid, _count, _showstate, _showtype]
        _msg = {"id": MsgDefine.GAME_MSG_GETITEMTIP, "data": _data}
        await self.ToClientMsg(_msg)

    # 商店购买
    # _type =1 礼包商店
    # _type =3 钻石商店
    # _type =4 金币商店

    async def C_shopbuy(self, _type, _index):
        # print("C_shopbuy", _type, _index)
        if _type == 1:  # 礼包商店
            await self.shopby_gift(_index)

        elif _type == 3:  # 钻石商店
            if _index < 0 or _index > 4:  # 索引错误
                return False
            _val = ConfigData.shoplist3_con[_index]
            if len(_val) != 2:
                return False
            _coust = _val[0]
            _give = _val[1]
            # 增加钻石
            await self.add_paymoney(_give)

        elif _type == 4:  # 金币商店
            if _index < 0 or _index > 4:  # 索引错误
                return False
            _val = ConfigData.shoplist4_con[_index]
            if len(_val) != 2:
                return False
            _coust = _val[0]
            _give = _val[1]

            # 扣除钻石
            await self.rec_paymoney(_coust)
            # 增加金币
            await self.add_gamemoney(_give)

    # 礼包商城
    async def shopby_gift(self, _index):
        _data = ConfigData.libao_Data[_index]
        if (_data == None):
            return False
        rewardType = eval(_data["rewardType"])
        rewardPra = eval(_data["rewardPra"])
        _nums = 0
        for _type in rewardType:
            _arr = rewardPra[_nums]
            await self.AddItem(_type, _arr, 0, 1)
            _nums = _nums + 1

    # 添加物品
    # _type 类型
    # _arr 奖励数据
    # _showitemtioc 是否显示[1:显示，0：不显示]
    # _showtype 显示类型[1正常需要显示的，2：等级显示的，3：签到显示的]
    async def AddItem(self, _type, _arr, _showitemtioc, _showtype):

        _id = 0
        _count = 0
        if (_type == 1):  # 奖励金币
            _count = _arr[0]
            await self.add_gamemoney(_count)

        elif (_type == 2):  # 奖励钻石
            _count = _arr[0]
            await self.add_paymoney(_count)

        elif (_type == 5):  # 奖励种子
            _random = random.randint(_arr[0], _arr[1])
            _id = _random
            _seeddata = ConfigData.seed_Data[_id]
            if _seeddata is None:
                print("奖励种子找不到" + str(_id))
                return False
            _count = _arr[2]

            await self.Add_seed(_id, _count)  # 增加种子

        elif (_type == 7):  # 奖励衣服

            _minid = str(_arr[0])[0:3]
            _maxid = str(_arr[1])[0:3]

            _minnum = str(_arr[0])[-1]
            _maxnum = str(_arr[1])[-1]

            _random1 = random.randint(int(_minid), int(_maxid))
            _random2 = random.randint(int(_minnum), int(_maxnum))

            _id = _random1 * 100 + _random2
            _count = _arr[2]
            _dressdata = ConfigData.dress_Data[_id]
            if _dressdata is None:
                print("奖励衣服找不到" + str(_id))
                return False
            await self.add_suit(_id, "award")  # 增加衣服
            await self.sold_moresuit()  # 出售多余的衣服

        elif (_type == 9):  # 奖励套装

            # 已经拥有的套装数据
            _havesuitListkey_str = self.suitlist.keys()
            _havesuitListkey = [int(i) for i in _havesuitListkey_str]
            # print("_havesuitListkey", _havesuitListkey)
            # A-S配表套装数据
            _consuitListKey = ConfigData.A_S_suitlistid

            # 没有集齐任意一件的套装id
            _nolist = []
            for _conval in _consuitListKey:
                if (_conval not in _havesuitListkey):
                    _nolist.append(_conval)
            # print("_nolist1", _nolist)
            # print("_consuitListKey", _consuitListKey)
            # 套装全部拥有判断是否有配件没集齐
            _havesuitlistdata = []
            if len(_nolist) <= 0:
                for _key in self.suitlist.keys():
                    if (int(_key) in _consuitListKey):  # 必须是A-S的套装
                        _val = self.suitlist[_key]
                        if (len(_val) < 9):
                            _tmpval = [int(_key), len(_val)]
                            _havesuitlistdata.append(_tmpval)
            # print("_havesuitlistdata1", _havesuitlistdata)
            # 已集齐没有集齐全部的做个数组按照数量排序
            if (len(_havesuitlistdata) > 0):
                sorted(_havesuitlistdata, key=(lambda x: x[1]), reverse=True)
                _id = _havesuitlistdata[0][0]
                _countmin = _havesuitlistdata[0][1]
                if (_countmin < 9):
                    _nolist.append(_id)
            # print("_havesuitlistdata2", _havesuitlistdata)
            # print("_nolist1", _nolist)
            # 没有的套装数据
            if (len(_nolist) <= 0):
                _msg = {"id": 0, "data": "你已经集齐A级或者A级以上所有套装"}
                await self.To_C_Tips(_msg)
                return
            _random = random.randint(0, len(_nolist) - 1)
            _id = _nolist[_random]
            _count = _arr[2]
            # if (_id not in _arr):
            #     return False
            _suitdata = ConfigData.suit_Data[_id]
            if _suitdata is None:
                print("奖励套装找不到" + str(_id))
                return False
            dressIds = eval(_suitdata["dressIds"])
            for _val in dressIds:
                await self.add_suit(_val, "award")  # 增加衣服
                await self.sold_moresuit()  # 出售多余的衣服

        # 物品提示数据
        await self.showitemtips(_type, _id, _count, _showitemtioc, _showtype)

    # 免费商店领取种子
    async def c_freeshop(self, _index):
        _val = ConfigData.free_shop[_index]
        if (_val == None or len(_val) < 3):
            return False

        _itemid = _val[0]
        _seedid = _itemid
        _count = _val[1]
        await self.Add_seed(_seedid, _count)  # 增加种子
        await self.showitemtips(5, _seedid, _count, 1, 1)

    # 设置限时种子商店数据
    async def set_timeseeddata(self):

        _min = time.localtime().tm_min  #获取当前系统时间分钟
        _sec = time.localtime().tm_sec  #获取当前时间秒钟
        _tmptimes = 0
        if _min < 31:
            _tmptimes = 30 - _min
        else:
            _tmptimes = 60 - _min
        for i in range(2):
            _list = []
            if len(self.timeseeddata) == 2:
                _list = self.timeseeddata[str(i)]
            # print("timeseeddata", self.timeseeddata)
            if (len(_list) != 4):
                _seedid = random.randint(1001, 1036)
                _time = int(time.time() - _sec)
                _longtime = _tmptimes
                _buycount = 0
                _list = [_seedid, _time, _longtime, _buycount]
                self.timeseeddata[str(i)] = _list
            elif (len(_list) == 4):
                _oldtime = _list[1]
                _oldlong = _list[2]
                _time = _oldtime + _oldlong * 60
                print(_time, int(time.time()))
                if (time.time() >= _time):
                    _seedid = random.randint(1001, 1036)
                    _time = int(time.time() - _sec)
                    _longtime = _tmptimes
                    _buycount = 0
                    _list = [_seedid, _time, _longtime, _buycount]
                    self.timeseeddata[str(i)] = _list

        await self.send_timeseeddata()

    # 限时种子购买
    async def client_buytimeseed(self, _index):
        _list = self.timeseeddata[str(_index)]
        if (_list == None):
            return False
        if (len(_list) != 4):
            return False
        _seedid = _list[0]
        # 限时购买种子
        if (_index == 0):
            _seeddata = ConfigData.seed_Data[_seedid]
            if (_seeddata["id"] < 1000):
                return
            _moneytype = _seeddata["buyType"]
            _needmoney = int(_seeddata["price"] * 1 * 0.7)
            # 游戏币不足
            if (_moneytype == 1):
                if (await self.get_gamemoney() < _needmoney):  # 货币不足
                    # 发送消息货币不足
                    await self.SendToClientTips(101002)
                    return False
            # 钻石
            elif (_moneytype == 2):
                if (await self.get_paymoney() < _needmoney):  # 货币不足
                    # 发送消息货币不足
                    await self.SendToClientTips(101003)
                    return False
            _addseedstate = await self.Add_seed(_seedid, 1)
            _state = False
            # 种子数据增加成功
            if (_addseedstate):
                if (_moneytype == 1):
                    _state = await self.rec_gamemoney(_needmoney)
                elif (_moneytype == 2):
                    _state = await self.rec_paymoney(_needmoney)
            if (_state):
                await self.Sendseeddata()
        elif (_index == 1):
            _addseedstate = await self.Add_seed(_seedid, 1)
            await self.Sendbasedata()

        # 成功
        if _addseedstate:
            _list[3] += 1
            self.timeseeddata[str(_index)] = _list
            await self.send_timeseeddata()
