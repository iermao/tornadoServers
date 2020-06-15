# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 玩家模块 ----会继承其他几个模块

import os
import json
import time
import hashlib
import tornado

from .model.Player import Player
from .model.DBmanage import dbmanage

from .model import ConfigData

MSG_STARTGAME = 10001


# 游戏管理
class game(object):
    def __init__(self):
        print("Game  __init__")
        # 所有连接进来的网络对象
        self.nobjlist = set()
        # 创建的玩家字典
        self.playerList = dict()
        # 需要删除的玩家列表
        self.deletecidlist = []
        # 实例化数据库连接对象
        self.dbmanage = dbmanage()
        # 初始化配置数据
        ConfigData.init()

        self.starttime = time.time()

        self.printtime = time.time()

        tornado.ioloop.PeriodicCallback(self.loopTimer, 1000).start()

    # 创建新链接用户
    async def loopTimer(self):
        _time = time.time()
        _mins = int((_time - self.starttime) / 60)  # 运行时间
        _nextpainttime = _time - self.printtime
        if (_nextpainttime > 10):
            self.printtime = time.time()
            print("Server Start {0} mins, pid [{1}], nobjlist [{2}], plist [{3}]".format(str(_mins), str(os.getpid()), str(len(self.nobjlist)), str(len(self.playerList))))

        await self.CleanUser()

    # 用户下线操作
    async def CleanUser(self):
        _time = time.time()

        for _pUser in self.playerList.values():
            await _pUser.loopTimer()
            # 心跳检测1分钟没链接则掉线
            if (_pUser.herttime + 60 * 1) < _time:
                self.deletecidlist.append(_pUser.cid)

        for _cid in self.deletecidlist:
            if (_cid not in self.playerList.keys()):
                continue
            _pUser = self.playerList[_cid]
            if (_pUser is None):
                continue
            await _pUser.close()
            await _pUser.SaveData_ALL()
            await self.DelPlayerList(_pUser.pobj)
            # 已经删除会报错异常，这里异常抛出
            try:
                self.nobjlist.remove(_pUser.pobj)
            except:
                pass
                # self.nobjlist.remove(_pUser.pobj)

        self.deletecidlist.clear()

    async def NewUser(self, nobj):

        # 取得用户数据，根据socket第一次连接传递过来数据进行验证

        uid = nobj.current_user.uid

        if (uid == "" or uid == "None" or uid == None):
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
        puid = await self.dbmanage.selUser(_uid, _pwd)

        if (puid < 1):
            return False, " puid err" + str(puid)

        nobj.current_user.cid = puid
        # print("11111111111")

        checkobj = await self.GetPlayer(nobj)

        if (checkobj != None):
            # 用户没有下线
            print("checkobj 1 ")
            self.deletecidlist.append(puid)
            await self.CleanUser()

        print("NewUser nobjlist length---step 1  ", len(self.nobjlist))

        await self.PListInsert(nobj)

        print("NewUser nobjlist length---step 2  ", len(self.nobjlist))

        _msg = {"id": MSG_STARTGAME}
        await self.ClientMsg(nobj, _msg)
        return True, " link ok "

    # *****************************
    # 玩家列表管理-------------begin
    # *****************************

    # 玩家列表增加数据
    async def PListInsert(self, nobj):
        _cid = nobj.current_user.cid
        _pwd = nobj.current_user.pwd
        if (_cid in self.playerList.keys()):
            return self.playerList[nobj.current_user.cid]

        # 增加到socket连接用户列表
        self.nobjlist.add(nobj)
        # 实例化一个玩家对象
        puser = Player()
        await puser.init(nobj, _cid, _pwd, self.dbmanage)
        # 玩家列表增加玩家对象
        self.playerList[_cid] = puser

        return self.playerList[_cid]

    #根据连接对象返回玩家实例
    async def GetPlayer(self, nobj):
        if (nobj.current_user.cid in self.playerList.keys()):
            return self.playerList[nobj.current_user.cid]
        return None

    # 删除玩家实例
    async def DelPlayerList(self, nobj):
        if (nobj.current_user.cid in self.playerList.keys()):
            self.playerList.pop(nobj.current_user.cid)
            return True
        return False

    # *****************************
    # 玩家列表管理-------------end
    # *****************************

    # *****************************
    # 消息管理
    # *****************************
    async def ServerMsg(self, nobj, msg):

        # print(len(self.playerList))

        _player = await self.GetPlayer(nobj)
        if (_player != None):
            try:
                _msg = json.loads(msg)
            except Exception as e:
                print("json err ", str(e))
                return
            await _player.ClientToServer(msg)
            # try:
            #     _player.ClientToServer(_msg)
            # except Exception as e:
            #     print("ServerMsg err {0}".format(str(e)))

    #给客户端发送消息
    async def ClientMsg(self, nobj, _msg=""):
        if (_msg == ""):
            _msg = {"id": MSG_STARTGAME}
        await nobj.write_message(_msg)

    async def close(self, nobj):
        # print("close")
        if (nobj in self.nobjlist):
            print("close 11  ")
            print(nobj.current_user.uid, " close")
            puser = self.playerList[nobj.current_user.cid]
            if (puser != None):
                print("close 22  ")
                await puser.close()
                await puser.SaveData_ALL()
            await self.DelPlayerList(nobj)
            nobj.close()
            # 已经删除会报错异常，这里异常抛出
            try:
                self.nobjlist.remove(nobj)
            except:
                pass
