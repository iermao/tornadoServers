# import os
# import json
# import datetime
import hashlib

from .model.Player import Player
from .model.DBmanage import dbmanage

MSG_STARTGAME = 10001


# 游戏管理
class game():
    def __init__(self):
        print("Game  __init__")
        # 所有连接进来的网络对象
        self.nobjs = set()
        # 创建的玩家字典
        self.playerList = dict()
        # 实例化数据库连接对象
        self.dbmanage = dbmanage()
        pass

    # 创建新链接用户

    def NewUser(self, nobj):
        if nobj in self.nobjs:
            return False, "on link"

        # 取得用户数据，根据socket第一次连接传递过来数据进行验证
        if (nobj.current_user.uid == "" or nobj.current_user.uid == "None" or nobj.current_user.uid == None):
            return False, " nobj.current_user none or empty"

        _uid = nobj.current_user.uid
        _pwd = nobj.current_user.pwd
        _keys = nobj.current_user.keys
        puid = -1
        if (_uid == "" or _keys == ""):
            return False, " _uid,_keys empty"

        # 解析出来用户名和密码
        _tmpstr = (_uid + "wowadmin+=-09").encode(encoding='UTF-8')
        _tmpkey = hashlib.md5(_tmpstr).hexdigest()
        # 校验数据
        if (_tmpkey != _keys):
            return False, " _keys err"
        # 查询用户匹配数据
        puid = self.dbmanage.selUser(_uid, _pwd)

        if (puid < 1):
            return False, " puid err" + str(puid)

        nobj.current_user.cid = puid
        print("11111111111")

        print(nobj.current_user.cid)

        self.PListInsert(nobj)

        _msg = {"id": MSG_STARTGAME}
        self.ClientMsg(nobj, _msg)
        return True, " link ok "

    # *****************************
    # 玩家列表管理-------------begin
    # *****************************

    # 玩家列表增加数据
    def PListInsert(self, nobj):
        _cid = nobj.current_user.cid
        _pwd = nobj.current_user.pwd
        if (_cid in self.playerList.keys()):
            return self.playerList[nobj.current_user.cid]

        # 增加到socket连接用户列表
        self.nobjs.add(nobj)
        # 实例化一个玩家对象
        puser = Player(nobj, _cid, _pwd, self.dbmanage)
        # 玩家列表增加玩家对象
        self.playerList[_cid] = puser

        return self.playerList[_cid]

    #根据连接对象返回玩家实例
    def GetPlayer(self, nobj):
        if (nobj.current_user.cid in self.playerList.keys()):
            return self.playerList[nobj.current_user.cid]
        return None

    # 删除玩家实例
    def DelPlayerList(self, nobj):
        if (nobj.current_user.cid in self.playerList.keys()):
            self.playerList.pop(nobj.current_user.cid)
            return True
        return False

    # *****************************
    # 玩家列表管理-------------end
    # *****************************

    def ServerMsg(self, nobj, _msg):

        print(len(self.playerList))

        if nobj in self.playerList:
            print("TS----------")
        else:
            pass
        # print("TS")
        pass

    #给客户端发送消息
    def ClientMsg(self, nobj, _msg=""):
        if (_msg == ""):
            _msg = {"id": MSG_STARTGAME}
        nobj.write_message(_msg)

    def close(self, nobj):
        print("close")
        if (nobj in self.nobjs):
            self.nobjs.remove(nobj)
            puser = self.playerList[nobj.current_user.cid]
            if (puser != None):
                puser.SaveData()
            self.DelPlayerList(nobj)
