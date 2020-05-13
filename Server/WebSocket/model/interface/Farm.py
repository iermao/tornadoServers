import json
import time
import random

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData

from tornado import gen


class Farm(object):
    def __init__(self):

        # 初始化植物数据
        self.plantdata = {}
        # 初始化种子数据
        self.seeddata = {}

        self.plantobj = dict()
        # pass

    async def init(self):
        pass

    # 发送土地植物数据
    async def Sendplantdata(self):
        _msg = {"id": MsgDefine.USER_MSG_PLANTDATA, "data": self.plantdata}
        await self.ToClientMsg(_msg)

    # 发送种子数据
    async def Sendseeddata(self):

        _msg = {"id": MsgDefine.USER_MSG_SEEDDATA, "data": self.seeddata}
        await self.SetobjPlantData()

        await self.ToClientMsg(_msg)

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
                return False
        # 钻石
        elif (_moneytype == 2):
            if (await self.get_paymoney() < __needmoney):  # 货币不足
                # 发送消息货币不足
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
            return True
        else:
            self.seeddata[key] = count
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
            return True
        else:
            return False

    # 土地种植种子
    async def C_Plant_seed(self, plantindex, seedid):
        if (await self.have_seed(seedid) is True):
            _plantobj = self.plantobj[plantindex]
            if (_plantobj != None and _plantobj.langstate == 1):
                _newPlant = PlantData()
                await _newPlant.init()
                await _newPlant.newPlant(seedid)

                rec_seedstate = await self.Rec_seed(seedid, 1)
                if (rec_seedstate):
                    self.plantobj[plantindex] = _newPlant

        await self.SendOnePlant(plantindex)
        await self.Sendseeddata()

    # 状态按钮点击
    async def C_Plant_pick(self, plantindex):

        _plantobj = self.plantobj[plantindex]
        if (_plantobj != None):
            # print(self.cid, plantindex, _plantobj.seedid, await _plantobj.Toarr())
            if (_plantobj.moneystate == 1):
                _state = await _plantobj.pickmoney()
                if (_state == True):  # 加钱加经验
                    _money = await _plantobj.GetStep_rewardCoins()
                    _exp = await _plantobj.getstep_rewardExps()

                    await self.add_gamemoney(_money)
                    await self.addexp(_exp)
            elif (_plantobj.waterstate == 1):
                _state = await _plantobj.Water()

            # 收获这里要给玩家增加游戏币以及衣服数据
            elif (_plantobj.step == 4 and _plantobj.moneystate == 0 and _plantobj.waterstate == 0):
                seeddata = ConfigData.seed_Data[_plantobj.seedid]
                suitid = int(seeddata["suitId"])
                suitdata = ConfigData.suit_Data[suitid]
                dresslist = eval(suitdata["dressIds"])
                _random = random.randint(0, len(dresslist) - 1)
                _index = dresslist[_random]
                await self.add_suit(_index)
                await _plantobj.Harvest()
            else:
                pass
        await self.SendOnePlant(plantindex)

    # 检测是否完成
    async def C_Plant_check(self, plantindex):
        _plantobj = self.plantobj[plantindex]
        if (_plantobj != None):
            # print(self.cid, plantindex, _plantobj.seedid, await _plantobj.Toarr())
            await _plantobj.changeState()

        await self.SendOnePlant(plantindex)


class PlantData(object):

    langstate = -1  #(0:为开放，1：未种植，2:已经种植)
    seedid = 0  #种子id
    times = 0  #种植时间
    step = 0  #阶段状态
    steptimes = 0  #当前阶段已经进行时间
    moneystate = 0  #是否金钱奖励
    waterstate = 0  #是否需要浇水
    watertimes = 0  #浇水时间
    otherstate2 = 0
    otherstate3 = 0
    otherstate4 = 0

    def __init__(self):
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
        self.otherstate2 = _arr[8]
        self.otherstate3 = _arr[9]
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
        _dataarr.append(self.otherstate2)
        _dataarr.append(self.otherstate3)
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
        self.otherstate2 = 0
        self.otherstate3 = 0
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
    async def changeState(self):

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
        _neewtimes = float(self.watertimes / 1000.00) + float(_steptime)

        # print(_neewtimes, _steptime, _seeddata)
        if (_neewtimes <= time.time()):
            self.step += 1
            if (self.step == 4):
                self.moneystate = 1
            else:
                self.waterstate = 1
                self.moneystate = 1
            return True
        return False

    # 获取当前阶段需要时间
    async def GetStepTimes(self):
        # print(self.seedid)

        if (self.seedid < 1):
            return 0
        _seeddata = ConfigData.seed_Data[self.seedid]
        _arr = eval(_seeddata["growTime"])

        # print(_seeddata)
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
        self.otherstate2 = 0
        self.otherstate3 = 0
        self.otherstate4 = 0

        return True
