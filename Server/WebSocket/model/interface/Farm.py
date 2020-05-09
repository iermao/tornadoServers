import json
import time

from Server.WebSocket.model import MsgDefine


class Farm():

    # 初始化植物数据
    plantdata = {}
    # 初始化种子数据
    seeddata = {}

    def __init__(self):
        pass

    def Sendplantdata(self):
        _msg = {"id": MsgDefine.USER_MSG_PLANTDATA, "data": self.plantdata}
        self.pobj.write_message(_msg)

    def Sendseeddata(self):
        _msg = {"id": MsgDefine.USER_MSG_SEEDDATA, "data": self.seeddata}
        self.pobj.write_message(_msg)

    # 购买种子
    def bny_seed(self, seedid, count, moneytype):
        # 需要货币数量
        __needmoney = 0

        # 游戏币不足
        if (moneytype == 1):
            if (self.get_gamemoney() < __needmoney):  # 货币不足
                # 发送消息货币不足
                return False
        # 钻石
        if (moneytype == 2):
            if (self.get_paymoney() < __needmoney):  # 货币不足
                # 发送消息货币不足
                return False

        _addseedstate = self.Add_seed(seedid, count)

        if (_addseedstate):
            if (moneytype == 1):
                self.rec_gamemoney(__needmoney)
            if (moneytype == 2):
                self.rec_paymoney(__needmoney)

    # 增加种子
    def Add_seed(self, seedid, count):
        if (count <= 0):
            return False
        if (seeddata.get(str(seedid), default=0) > 0):
            seeddata[seedid] += count
            return True
        else:
            seedid[str(seedid)] = count
            return True

    # 种子减少
    def Rec_seed(self, seedid, count):
        if (count <= 0):
            return False
        if (seeddata.get(str(seedid), default=0) > 0):
            seeddata[seedid] += count
            return True
        else:
            seedid[str(seedid)] = count
            return True