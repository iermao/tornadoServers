
import json
import time

from Server.WebSocket.model import MsgDefine



# 用户基础对象
class BaseUser(object):

    def __init__(self, _user, cid, _DBM):
        print("User  __init__")
        self.cid = cid
        self.pobj = _user
        self.logintime = time.time()*1000
        self.logouttime = time.time()*1000
        self.DBM = _DBM

        # 初始化数据
        self.initData()
    def close(self):
        self.logouttime = time.time()*1000
    #初始化部分数据
    def initData(self):
        # 初始化玩家数据
        self.DBM.initplayerdata(self.cid)

    # 接受消息
    def ClientToServer(self,msg):
        # print(str(msg))
        try:
            _msg = json.loads(msg)
        except:
            print("json 解析报错！")
            return
        # print(_msg)
        _msgid = int(_msg["id"])
        # print("ClientToServer",_msgid,type(_msg["data"]),_msg["data"])

        if(_msgid == MsgDefine.USER_MSG_BUYSEED):# 购买种子
            self.client_buyseed(_msg["data"])

        elif(_msgid == MsgDefine.USER_MSG_PLANT):# 种植
            self.client_plantnew(_msg["data"])
  
        elif(_msgid == MsgDefine.USER_MSG_PLANT_PICK):# 植物状态按钮点击
            self.client_plantpick(_msg["data"])

        elif(_msgid == MsgDefine.USER_MSG_PLANT_CHECK):# 植物状态检测
            self.client_plantcheckstate(_msg["data"])

        elif(False):
            pass
        else:
            pass
        
    # 给客户端发送消息
    def ToClientMsg(self, msg):
        pass
    # **********************************************************
    # 客户端消息处理
    # **********************************************************
    # 买种子
    def client_buyseed(self,msg):
        _seedid = msg['seedid']
        _count = msg["count"]
        self.C_buy_seed(_seedid,_count)

    # 种植土地
    def client_plantnew(self,msg):
        index=int(msg['index'])
        seedid = msg["seedid"]
        self.C_Plant_seed(index, seedid)
    # 土地状态点击
    def client_plantpick(self,msg):
        index=int(msg['index'])
        self.C_Plant_pick(index)

    def client_plantcheckstate(self,msg):
        index=int(msg['index'])
        self.C_Plant_check(index)
