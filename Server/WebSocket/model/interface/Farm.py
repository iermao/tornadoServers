import json
import time

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData

from tornado import gen


class Farm():

    # 初始化植物数据
    plantdata = {}
    # 初始化种子数据
    seeddata = {}

    plantobj = dict()

    def __init__(self):
        aa = self.timer()
        pass
    
    
    def aaa(self):
        self.timer()

    async def timer(self):
        await gen.sleep(10)
        print("timer", self.cid)
        for obj in self.plantobj.values():
            if (obj.langstate == 1):
                pass
            else:
                pass
        self.timer()

    # 发送土地植物数据
    def Sendplantdata(self):
        _msg = {"id": MsgDefine.USER_MSG_PLANTDATA, "data": self.plantdata}
        self.pobj.write_message(_msg)

    # 发送种子数据
    def Sendseeddata(self):

        _msg = {"id": MsgDefine.USER_MSG_SEEDDATA, "data": self.seeddata}

        self.pobj.write_message(_msg)
        self.SetobjPlantData()

    # 发送一个土地数据
    def SendOnePlant(self, index):
        _plantobj = self.plantobj[index]  # 获取对象
        self.plantdata[str(index)] = _plantobj.Toarr()  # 转化数据
        _data = {"id": index, "val": _plantobj.Toarr()}  #拼接数据
        _msg = {"id": MsgDefine.USER_MSG_PLANT_ONE, "data": _data}
        self.pobj.write_message(_msg)  # 发送数据

    # 将土地数据设置为对象
    def SetobjPlantData(self):
        for key in self.plantdata.keys():
            _nkey = int(key)
            # print(self.plantdata[key])
            _newplantdata = PlantData(self.plantdata[key])
            self.plantobj[_nkey] = _newplantdata
        # print(self.plantobj)

    # 将土地数据设置为存库对象
    def SetDataPlantobj(self):
        pass

    # 购买种子
    def C_buy_seed(self, _seedid, _count):
        # 需要货币数量
        _seeddata = ConfigData.seed_Data[_seedid]
        if (_seeddata["id"] < 1000):
            return
        _moneytype = _seeddata["buyType"]

        __needmoney = _seeddata["price"] * _count
        # 游戏币不足
        if (_moneytype == 1):
            if (self.get_gamemoney() < __needmoney):  # 货币不足
                # 发送消息货币不足
                return False
        # 钻石
        elif (_moneytype == 2):
            if (self.get_paymoney() < __needmoney):  # 货币不足
                # 发送消息货币不足
                return False

        _addseedstate = self.Add_seed(_seedid, _count)

        _state = False
        # 种子数据增加成功
        if (_addseedstate):
            if (_moneytype == 1):
                _state = self.rec_gamemoney(__needmoney)
            elif (_moneytype == 2):
                _state = self.rec_paymoney(__needmoney)
        # 种子数据增加失败
        else:
            print("增加种子失败")
            pass

        if (_state):
            self.Sendseeddata()
            self.Sendbasedata()
        else:
            print("扣除货币失败")

    #判断是否有这个种子
    def have_seed(self, seedid):
        key = str(seedid)
        if (key in self.seeddata):
            return True
        else:
            return False

    # 增加种子
    def Add_seed(self, seedid, count):
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
    def Rec_seed(self, seedid, count):
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
    def C_Plant_seed(self, plantindex, seedid):
        if (self.have_seed(seedid) is False):
            return False

        _plantobj = self.plantobj[plantindex]

        if (_plantobj == None):
            return False
        # 不能种植
        if (_plantobj.langstate != 1):
            return False

        _newPlant = PlantData()
        _newPlant.newPlant(seedid)

        rec_seedstate = self.Rec_seed(seedid, 1)
        if (rec_seedstate):
            self.plantobj[plantindex] = _newPlant
            self.SendOnePlant(plantindex)
            self.Sendseeddata()

    # 状态按钮点击
    def C_Plant_pick(self, plantindex):
        _plantobj = self.plantobj[plantindex]
        if (_plantobj == None):
            return False
        if (_plantobj.moneystate == 1):
            _state = _plantobj.pickmoney()
            if (_state == True):  # 加钱加经验
                _money = _plantobj.GetStep_rewardCoins()
                _exp = _plantobj.getstep_rewardExps()

                self.add_gamemoney(_money)
                self.addexp(_exp)
                pass
        elif (_plantobj.waterstate == 1):
            _state = _plantobj.Water()
        # 收获这里要给玩家增加游戏币以及衣服数据
        elif (_plantobj.step == 4):
            _state = _plantobj.Harvest()
        else:
            pass

        self.SendOnePlant(plantindex)

    # 检测是否完成
    def C_Plant_check(self, plantindex):
        _plantobj = self.plantobj[plantindex]
        if (_plantobj == None):
            return False
        print(self.cid, plantindex, _plantobj.seedid)
        state = _plantobj.changeState()
        if (state):
            self.SendOnePlant(plantindex)
        else:
            return False


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

    def __init__(self, _arr=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
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

    def Toarr(self):
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
    def newPlant(self, _seedid):
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
    def Water(self):
        if (self.waterstate == 1):
            self.waterstate = 0
            self.steptimes = 0
            self.watertimes = time.time() * 1000
            return True
        return False

    # 收获
    def pickmoney(self):
        if (self.moneystate == 1):
            self.moneystate = 0
            return True
        else:
            return False

    #  检测状态
    def changeState(self):

        if (self.step == 4):
            return False

        if (self.waterstate == 1):
            return False

        if (self.moneystate == 1):
            return False

        _steptime = self.GetStepTimes()

        if (_steptime <= 0):
            return False

        print(self.watertimes, _steptime)
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
    def GetStepTimes(self):
        print(self.seedid)

        if (self.seedid < 1):
            return 0
        _seeddata = ConfigData.seed_Data[self.seedid]
        _arr = eval(_seeddata["growTime"])

        # print(_seeddata)
        _data = _arr[self.step]

        return _data

    # 获取当前阶段奖励金币
    def GetStep_rewardCoins(self):
        if (self.seedid < 1):
            return None
        _seeddata = ConfigData.seed_Data[self.seedid]
        _arr = eval(_seeddata["rewardCoins"])
        _data = _arr[self.step - 1]
        return _data

    # 获取经验
    def getstep_rewardExps(self):
        if (self.seedid < 1):
            return None
        _seeddata = ConfigData.seed_Data[self.seedid]
        _arr = eval(_seeddata["rewardExps"])
        _data = _arr[self.step - 1]
        return _data

    # 获取声望
    def getstep_sw(self):
        return 5

    # 收获
    def Harvest(self):
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
