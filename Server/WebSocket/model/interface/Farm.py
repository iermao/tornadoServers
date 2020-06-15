# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 花园模块

import json
import time
import random

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData

from tornado import gen


class Farm(object):
    def __init__(self):

        # 所有种植过的植物数据
        self.allplantdata = {}

        # 初始化植物数据
        self.plantdata = {}
        # 初始化种子数据
        self.seeddata = {}

        self.plantobj = dict()
        # pass

    async def init(self):
        pass

    async def initData(self):
        # 当前种植的植物数据
        _plantdata = await self.DBM.getSeedAndPlantData(self.cid)
        self.plantdata = _plantdata["plantdata"]
        self.seeddata = _plantdata["seeddata"]

        # 未完成新手教学则将第三块土地数据重置
        _guidestate = await self.get_guide()
        if _guidestate == 0:
            self.plantdata["2"] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        _alldata = await self.DBM.getallplantdata(self.cid)
        self.allplantdata = _alldata["data"]

        await self.Sendplantdata()
        await self.Sendseeddata()

        await self.sendallplantdata()

    # 保存数据
    async def SaveData(self):
        await self.DBM.Save_farmdata(self)
        await self.DBM.save_allplantdata(self)

    # 发送土地植物数据
    async def Sendplantdata(self):
        _msg = {"id": MsgDefine.USER_MSG_PLANTDATA, "data": self.plantdata}
        await self.ToClientMsg(_msg)

    # 发送种子数据
    async def Sendseeddata(self):

        _msg = {"id": MsgDefine.USER_MSG_SEEDDATA, "data": self.seeddata}
        await self.SetobjPlantData()

        await self.ToClientMsg(_msg)

# 声望相关记录
#发送所有种植数据[种子种植次数以及声望]

    async def sendallplantdata(self):
        _msg = {"id": MsgDefine.USER_MSG_ALLPLANTDATA, "data": self.allplantdata}
        await self.ToClientMsg(_msg)

    # 所有种植数据增加种植次数
    async def addplantnums(self, _seedid):
        _arr = None
        if str(_seedid) in self.allplantdata.keys():
            _arr = self.allplantdata[str(_seedid)]
        _newall = Seeddata()
        if (_arr is None):
            _newall.init_nw(_seedid)
            _newall.add_plant()
        else:
            _newall.init_db(_arr)
            _newall.add_plant()
        _tmparr = _newall.Toarr()
        self.allplantdata[str(_seedid)] = _tmparr

        await self.sendallplantdata()

    # 增加声望
    async def addshengwangnums(self, _seedid, _counts):
        _arr = None
        if str(_seedid) in self.allplantdata.keys():
            _arr = self.allplantdata[str(_seedid)]
        _newall = Seeddata()
        if (_arr is None):
            _newall.init_nw(_seedid)
            _newall.add_shengwang(_counts)
        else:
            _newall.init_db(_arr)
            _newall.add_shengwang(_counts)

        _tmparr = _newall.Toarr()
        self.allplantdata[str(_seedid)] = _tmparr

        _seeddata = ConfigData.seed_Data[_seedid]
        _name = _seeddata["name_cn"]
        _msg = {"id": 0, "data": "" + _name + "声望x" + str(_counts)}
        await self.To_C_Tips(_msg)

        await self.sendallplantdata()

        _counts = 0
        for _val in self.allplantdata.values():
            if (_val[2] >= 5000):
                _counts = _counts + 1
        await self.do_achieve_bytype(11, _counts)  # 触发成就---声望达到多少个


#
# 发送一个土地数据

    async def SendOnePlant(self, index):
        _plantobj = self.plantobj[index]  # 获取对象
        self.plantdata[str(index)] = await _plantobj.Toarr()  # 转化数据
        _data = {"id": index, "val": self.plantdata[str(index)]}  #拼接数据
        _msg = {"id": MsgDefine.USER_MSG_PLANT_ONE, "data": _data}
        # print(type(_msg))
        # print(_msg)
        # _smsg = json.dumps(_msg)
        await self.ToClientMsg(_msg)

    # 发送变异数据
    async def SendVariate(self, _oldid, _newid):
        _data = {"id1": _oldid, "id2": _newid}  #拼接数据
        _msg = {"id": MsgDefine.USER_MSG_SEEDVARIATE, "data": _data}
        await self.ToClientMsg(_msg)

    # 将土地数据设置为对象
    async def SetobjPlantData(self):
        for key in self.plantdata.keys():
            _nkey = int(key)
            _newplantdata = PlantData()
            await _newplantdata.init(self.plantdata[key])
            self.plantobj[_nkey] = _newplantdata
        # print(self.plantobj)

    # 将土地数据设置为存库对象
    async def SetDataPlantobj(self):
        pass

    # 购买种子
    async def C_buy_seed(self, _seedid, _count):
        # 需要货币数量
        _seeddata = ConfigData.seed_Data[_seedid]
        if (_seeddata["id"] < 1000):
            return
        _moneytype = _seeddata["buyType"]

        __needmoney = _seeddata["price"] * _count
        # 游戏币不足
        if (_moneytype == 1):
            if (await self.get_gamemoney() < __needmoney):  # 货币不足
                # 发送消息货币不足
                await self.SendToClientTips(101002)
                return False
        # 钻石
        elif (_moneytype == 2):
            if (await self.get_paymoney() < __needmoney):  # 货币不足
                # 发送消息货币不足
                await self.SendToClientTips(101003)
                return False

        _addseedstate = await self.Add_seed(_seedid, _count)

        _state = False
        # 种子数据增加成功
        if (_addseedstate):
            if (_moneytype == 1):
                _state = await self.rec_gamemoney(__needmoney)
            elif (_moneytype == 2):
                _state = await self.rec_paymoney(__needmoney)
        # 种子数据增加失败
        else:
            print("增加种子失败")
            pass

        if (_state):
            await self.Sendseeddata()
            await self.Sendbasedata()
        else:
            print("扣除货币失败")

    #判断是否有这个种子
    async def have_seed(self, seedid):
        key = str(seedid)
        if (key in self.seeddata):
            return True
        else:
            return False

    # 增加种子
    async def Add_seed(self, seedid, count):
        if (count <= 0):
            return False
        key = str(seedid)
        if (key in self.seeddata):
            self.seeddata[key] += count
        else:
            self.seeddata[key] = count

        _seeddata = ConfigData.seed_Data[seedid]

        _seedname = _seeddata["name_cn"]
        _msg = {"id": 0, "data": "获得{0}x{1}".format(_seedname, count)}
        await self.To_C_Tips(_msg)
        await self.Sendseeddata()

        return True

    # 种子减少
    async def Rec_seed(self, seedid, count):
        if (count <= 0):
            return False
        key = str(seedid)
        if (key in self.seeddata):
            self.seeddata[key] -= count
            if (self.seeddata[key] <= 0):
                self.seeddata.pop(key)

            await self.Sendseeddata()
            return True
        else:
            return False

    # 土地种植种子
    async def C_Plant_seed(self, plantindex, seedid):

        _state = False

        if (await self.have_seed(seedid) is True):
            _plantobj = self.plantobj[plantindex]
            if (_plantobj != None and _plantobj.langstate == 1):
                _newPlant = PlantData()
                await _newPlant.init()
                await _newPlant.newPlant(seedid)

                rec_seedstate = await self.Rec_seed(seedid, 1)
                if (rec_seedstate):
                    self.plantobj[plantindex] = _newPlant
                    _state = True

        await self.SendOnePlant(plantindex)
        await self.Sendseeddata()

        # 记录log
        if (_state):
            # 记录种植次数
            await self.do_achieve_bytype(2, 1)  # 触发成就---种植
            # await self.addplantnums(seedid)
            await self.DBM.log_plant(self, plantindex, seedid, "log_farm_plant")

        # 做任务类型为2的任务【种植】
        await self.do_task_type(2)

    # 状态按钮点击（浇水以及阶段奖励）
    async def C_Plant_pick(self, plantindex, _type):

        _plantobj = self.plantobj[plantindex]
        if (_plantobj != None):
            if (_type == 0):  # 收钱或者浇水
                if (_plantobj.moneystate == 1):
                    _state = await _plantobj.pickmoney()
                    if (_state == True):  # 加钱加经验
                        _money = await _plantobj.GetStep_rewardCoins()
                        _exp = await _plantobj.getstep_rewardExps()
                        await self.add_gamemoney(_money)
                        await self.addexp(_exp)
                        # 增加声望
                        if _plantobj.step == 4:
                            await self.addshengwangnums(_plantobj.seedid, 5)
                elif (_plantobj.waterstate == 1):
                    _state = await _plantobj.Water()
                else:
                    pass
            if (_type == 1):  # 加速
                _mins = await _plantobj.getnexttime()
                if (_mins > 0):
                    _needmoney = _mins * 2
                    _state = await self.rec_paymoney(_needmoney)
                    if (_state):
                        # 加速
                        await _plantobj.speed()
                        # 检测变异
                        _state2 = await _plantobj.variate()  #植物变异
                        if _state2:
                            await self.SendVariate(_plantobj.oldid, _plantobj.seedid)

        await self.SendOnePlant(plantindex)

    # 收获按钮点击
    async def C_Plant_Havest(self, plantindex, _type):
        _plantobj = self.plantobj[plantindex]
        if (_plantobj != None):
            # 收获这里要给玩家增加游戏币以及衣服数据
            if (_plantobj.step == 4 and _plantobj.moneystate == 0 and _plantobj.waterstate == 0):

                _seedid = _plantobj.seedid
                seeddata = ConfigData.seed_Data[_seedid]
                suitid = int(seeddata["suitId"])
                suitdata = ConfigData.suit_Data[suitid]
                dresslist = eval(suitdata["dressIds"])
                # 消耗金币收获
                if (_type == 1):
                    _money = seeddata["callGemsRate"]
                    _state = await self.rec_gamemoney(_money)
                    if (_state == False):
                        await self.SendToClientTips(101002)
                        return False
                    _giverandom = random.randint(0, 100)
                    if (_giverandom <= 50):
                        _random = random.randint(0, len(dresslist) - 1)
                        _index = dresslist[_random]
                    else:
                        _index = -1
                # 消耗钻石收获
                if (_type == 2):
                    _money = seeddata["callGems"]
                    _guidestate = await self.get_guide()
                    # 新手引导
                    if _guidestate == 0:
                        _money = 0
                    _state = await self.rec_paymoney(_money)
                    if (_state == False):
                        await self.SendToClientTips(101003)
                        return False
                    _random = random.randint(0, len(dresslist) - 1)
                    _index = dresslist[_random]

                    # 新手引导
                    if _guidestate == 0:
                        _index = 10101

                await self.add_suit(_index, "plant")
                await _plantobj.Harvest()
                # 记录log
                await self.DBM.log_plant(self, plantindex, _seedid, "log_farm_harvest")
                # 增加植物种植次数数据
                await self.addplantnums(_seedid)

                await self.do_achieve_bytype(3, 1)  # 触发成就---植物召唤

                await self.set_guide()

        await self.SendOnePlant(plantindex)

    # 检测是否完成
    async def C_Plant_check(self, plantindex):
        _plantobj = self.plantobj[plantindex]
        if (_plantobj != None):
            # print(self.cid, plantindex, _plantobj.seedid, await _plantobj.Toarr())
            _guidestate = await self.get_guide()
            # 不是新手引导
            # print("C_Plant_check1", _guidestate, _plantobj.step)
            if _guidestate == 1:
                _state = await _plantobj.changeState(False)
                # print("C_Plant_check11", _state, _plantobj.step)
                # if _state and _plantobj.step == 2:  #植物变异
                _state2 = await _plantobj.variate()  #植物变异
                if _state2:
                    await self.SendVariate(_plantobj.oldid, _plantobj.seedid)
            # 新手引导
            else:
                _state = await _plantobj.changeState(True)

        await self.SendOnePlant(plantindex)

    #开垦新的土地
    async def C_New_Plant(self, plantindex):
        _plantobj = self.plantobj[plantindex]
        if (_plantobj != None):
            if (_plantobj.langstate == 0):

                _type = ConfigData.land_Data[1000 + plantindex + 1]["unlocktype"]
                _money = ConfigData.land_Data[1000 + plantindex + 1]["unlocknumber"]
                _needtittle = ConfigData.land_Data[1000 + plantindex + 1]["unlockfame"]
                _nowtittle = ConfigData.level_Data[self.basedata["level"]]["fame"]

                if (_nowtittle < _needtittle):
                    await self.SendToClientTips(101098)
                    return False
                if (_type == 2):  # 消耗的是游戏币
                    _recstate = await self.rec_gamemoney(_money)
                elif (_type == 3):  # 消耗的是钻石
                    _recstate = await self.rec_paymoney(_money)
                if (_recstate):  # 消耗成功
                    _plantobj.langstate = 1
                    await self.SendOnePlant(plantindex)
                    # 提示消息
                    _msg = {"id": 0, "data": "土地开垦成功！"}
                    await self.To_C_Tips(_msg)


class PlantData(object):
    def __init__(self):
        self.langstate = -1  #(0:为开放，1：未种植，2:已经种植)
        self.seedid = 0  #种子id
        self.times = 0  #种植时间
        self.step = 0  #阶段状态
        self.steptimes = 0  #当前阶段已经进行时间
        self.moneystate = 0  #是否金钱奖励
        self.waterstate = 0  #是否需要浇水
        self.watertimes = 0  #浇水时间
        self.oldid = 0
        self.variatestate = 0
        self.otherstate4 = 0
        pass

    async def init(self, _arr=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
        self.langstate = _arr[0]
        self.seedid = _arr[1]
        self.times = _arr[2]
        self.step = _arr[3]
        self.steptimes = _arr[4]
        self.moneystate = _arr[5]
        self.waterstate = _arr[6]
        self.watertimes = _arr[7]
        self.oldid = _arr[8]
        self.variatestate = _arr[9]
        self.otherstate4 = _arr[10]

    async def Toarr(self):
        _dataarr = []
        _dataarr.append(self.langstate)
        _dataarr.append(self.seedid)
        _dataarr.append(self.times)
        _dataarr.append(self.step)
        _dataarr.append(self.steptimes)
        _dataarr.append(self.moneystate)
        _dataarr.append(self.waterstate)
        _dataarr.append(self.watertimes)
        _dataarr.append(self.oldid)
        _dataarr.append(self.variatestate)
        _dataarr.append(self.otherstate4)

        return _dataarr

    # //设置一个临时植物数据
    async def newPlant(self, _seedid):
        self.langstate = 2
        self.seedid = _seedid
        self.times = time.time() * 1000
        self.step = 0
        self.steptimes = 0
        self.moneystate = 0
        self.waterstate = 1
        self.watertimes = 0
        self.oldid = 0
        self.variatestate = 0
        self.otherstate4 = 0

        return self

    # 浇水
    async def Water(self):
        if (self.waterstate == 1):
            self.waterstate = 0
            self.steptimes = 0
            self.watertimes = time.time() * 1000
            return True
        return False

    # 收获
    async def pickmoney(self):
        if (self.moneystate == 1):
            self.moneystate = 0
            return True
        else:
            return False

    #  检测状态
    async def changeState(self, _state):

        if (self.step == 4):
            return False

        if (self.waterstate == 1):
            return False

        if (self.moneystate == 1):
            return False

        _steptime = await self.GetStepTimes()

        if (_steptime <= 0):
            return False

        # print(self.watertimes, _steptime)
        if _state:
            _needtimes = 0
        else:
            _needtimes = float(self.watertimes / 1000.00) + float(_steptime)

        # print(_neewtimes, _steptime, _seeddata)
        if (_needtimes <= time.time()):
            self.step += 1
            if (self.step == 4):
                self.moneystate = 1
            else:
                self.waterstate = 1
                self.moneystate = 1
            return True
        return False

    # 植物变异
    async def variate(self):
        if self.step != 2:
            return False
        if self.variatestate == 1:
            return False
        _tmpseeddata = ConfigData.seed_Data[self.seedid]
        # 是否能变异
        canVariate = _tmpseeddata["canVariate"]
        if (canVariate == 0):
            return False
        # 变异几率
        variateRate = _tmpseeddata["variateRate"]

        # 变异ID
        variateId = _tmpseeddata["variateId"]

        _random = random.randint(1, 100)
        # print("variate", _random)
        if (_random > 21):
            return False

        self.oldid = self.seedid
        self.variatestate = 1
        self.seedid = variateId
        return True

    # 获取剩余多少时间完成
    async def getnexttime(self):
        _now = time.time()
        _steptime = await self.GetStepTimes()

        if (_steptime <= 0):
            return 0

        _watertime = float(self.watertimes / 1000.00)

        _needtimes = (_watertime + _steptime) - _now
        if (_needtimes <= 0):
            return 0

        # //计算还需要多少分钟
        mins = int((_needtimes + 60) / 60)

        return mins

    # 加速
    async def speed(self):
        self.step += 1
        if (self.step == 4):
            self.moneystate = 1
        else:
            self.waterstate = 1
            self.moneystate = 1
        return True

    # 获取当前阶段需要时间
    async def GetStepTimes(self):
        # print(self.seedid)

        if (self.seedid < 1):
            return 0
        _seeddata = ConfigData.seed_Data[self.seedid]
        _arr = eval(_seeddata["growTime"])

        # print(_seeddata)
        if (self.step > 3):
            return 0
        _data = _arr[self.step]

        return _data

    # 获取当前阶段奖励金币
    async def GetStep_rewardCoins(self):
        if (self.seedid < 1):
            return None
        _seeddata = ConfigData.seed_Data[self.seedid]
        _arr = eval(_seeddata["rewardCoins"])
        _data = _arr[self.step - 1]
        return _data

    # 获取经验
    async def getstep_rewardExps(self):
        if (self.seedid < 1):
            return None
        _seeddata = ConfigData.seed_Data[self.seedid]
        _arr = eval(_seeddata["rewardExps"])
        _data = _arr[self.step - 1]
        return _data

    # 获取声望
    async def getstep_sw(self):
        return 5

    # 收获
    async def Harvest(self):
        self.langstate = 1
        self.seedid = 0
        self.times = 0
        self.step = 0
        self.steptimes = 0
        self.moneystate = 0
        self.waterstate = 0
        self.watertimes = 0
        self.oldid = 0
        self.variatestate = 0
        self.otherstate4 = 0

        return True


class Seeddata:
    def __init__(self):
        self.id = 0  # 种子ID
        self.plantnums = 0  # 种植次数
        self.shengwang = 0  # 声望

    def init_db(self, _arr):
        self.id = _arr[0]
        self.plantnums = _arr[1]
        self.shengwang = _arr[2]

    def init_nw(self, _id):
        self.id = _id
        self.plantnums = 0
        self.shengwang = 0

    #种植次数加1
    def add_plant(self):
        self.plantnums += 1

    #增加声望
    def add_shengwang(self, _val):
        self.shengwang += _val

    def Toarr(self):
        _data = []
        _data.append(self.id)
        _data.append(self.plantnums)
        _data.append(self.shengwang)
        return _data
