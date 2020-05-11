
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
        print(str(msg))
        try:
            _msg = json.loads(msg)
        except:
            print("json 解析报错！")
            return
        # print(_msg)
        _msgid = int(_msg["id"])
        # print(_msgid,type(_msg["data"]),_msg["data"])
        if(_msgid == MsgDefine.USER_MSG_BUYSEED):
            self.client_buyseed(_msg["data"])
        elif(False):
            pass
    
        else:
            pass
        
    # 给客户端发送消息
    def ToClientMsg(self, msg):
        pass
    def client_buyseed(self,msg):
        # print(msg)
        # _msg = json.loads(msg)
        _seedid = msg['seedid']
        _count = msg["count"]
        # print(_seedid)
        self.bny_seed(_seedid,_count)
