import json
import time

from Server.WebSocket.model import MsgDefine


class Suit():

    # 当前穿搭数据
    suitdata = []
    # 当前衣服物品数据
    dressdata = []

    def __init__(self):
        pass

    def Sendsuitdata(self):
        _msg = {"id": MsgDefine.USER_MSG_SUITATA, "data": self.suitdata}
        self.pobj.write_message(_msg)

    def Senddressdata(self):
        _msg = {"id": MsgDefine.USER_MSG_DRESSDATA, "data": self.dressdata}
        self.pobj.write_message(_msg)
