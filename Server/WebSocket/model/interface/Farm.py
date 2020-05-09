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