import json
import time

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData


class Farm():

    # 初始化植物数据
    plantdata = {}
    # 初始化种子数据
    seeddata = {}

    plantobj = dict()

    def __init__(self):
        pass

    def Sendplantdata(self):
        _msg = {"id": MsgDefine.USER_MSG_PLANTDATA, "data": self.plantdata}
        self.pobj.write_message(_msg)

    def Sendseeddata(self):

        _msg = {"id": MsgDefine.USER_MSG_SEEDDATA, "data": self.seeddata}

        self.pobj.write_message(_msg)
        self.SetobjPlantData()

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
    def bny_seed(self, _seedid, _count):
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
            return True
        else:
            return False

    # # 获取土地对象
    # def getplantdata(self, plantindex):

    #     key = str(plantindex)
    #     if (key in self.seeddata):
    #         return self.plantdata[key]
    #     else:
    #         return None

    # 土地种植种子
    def Plant_seed(self, seedid, plantindex):
        if (self.have_seed() is False):
            return False

        _plantobj = self.plantobj[plantindex]

        if (_plantobj == None):
            return False
        # 不能种植
        if (_plantobj.langstate != 1):
            return False

        _newPlant = PlantData()
        _plantobj = _newPlant.newPlant()
        # self.plantobj[plantindex]

    # 获取游戏币
    def pickmoney(self, plantindex):
        _plantobj = self.plantobj[plantindex]
        if (_plantobj == None):
            return False
        _plantobj.pickmoney()

    # 浇水
    def water(self, plantindex):
        _plantobj = self.plantobj[plantindex]
        if (_plantobj == None):
            return False
        _plantobj.Water()

    def ChangeState(self, plantindex):
        plantdata = self.getplantdata(plantindex)
        if (plantdata == None):
            return False
        pass


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
        _dataarr.push(self.langstate)
        _dataarr.push(self.seedid)
        _dataarr.push(self.times)
        _dataarr.push(self.step)
        _dataarr.push(self.steptimes)
        _dataarr.push(self.moneystate)
        _dataarr.push(self.waterstate)
        _dataarr.push(self.watertimes)
        _dataarr.push(self.otherstate2)
        _dataarr.push(self.otherstate3)
        _dataarr.push(self.otherstate4)

        return _dataarr

    # //设置一个临时植物数据
    def newPlant(self, _seedid):
        self.langstate = 0
        self.seedid = _seedid
        self.times = time.time * 1000
        self.step = 0
        self.steptimes = 0
        self.moneystate = 0
        self.waterstate = 1
        self.watertimes = 0
        self.otherstate2 = 0
        self.otherstate3 = 0
        self.otherstate4 = 0

    # 浇水
    def Water(self):
        if (self.waterstate == 1):
            self.waterstate = 0
            self.steptimes = 0
            self.watertimes = time.time * 1000

    # 收获
    def pickmoney(self):
        if (self.moneystate == 1):
            self.moneystate = 0

    #  检测状态
    def changeState(self):
        _seeddata = ConfigData.seed_Data[self.seedid]
        _steptime = _seeddata["growTime"][self.step]
        _neewtimes = self.watertimes / 1000.00 + _steptime

        if (_neewtimes >= time.time()):
            self.step += 1
            if (self.step == 4):
                self.moneystate = 1
            else:
                self.waterstate = 1
                self.moneystate = 1

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
