# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

# 玩家基础模块

import json
import time
from tornado import gen

from Server.WebSocket.model import MsgDefine

from Server.WebSocket.model import ConfigData


# 用户基础对象
class BaseUser(object):
    def __init__(self):
        pass

    async def init(self, _user, cid, _DBM):
        self.cid = cid
        self.pobj = _user
        self.logintime = time.time() * 1000
        self.logouttime = time.time() * 1000
        self.foronlinetime = time.time() * 1000  # 计算在线时间开始时间
        self.DBM = _DBM
        # 初始化数据
        await self.initInsertData()
        # 存档时间
        self.savetime = time.time()
        # 在线时间发送时间
        self.sendonline = time.time()

    async def loopTimer(self):
        await self.checkthememodel()
        await self.timersavedata()

    async def timersavedata(self):
        _times = time.time()
        # 每个用户自动存档时间5分钟
        if ((_times - self.savetime) / 60.0 >= 5):
            self.savetime = time.time()
            await self.SaveData_ALL()

        # 检测是否需要发送在线数据
        await self.checksendonlinetime()

    async def checksendonlinetime(self):
        _times = time.time()
        # 1分钟发送一次在线时间
        if ((_times - self.sendonline) / 60.0 >= 1):
            # 计算在线时间本次在线时间
            _online = (time.time() - self.foronlinetime / 1000) / 60
            self.basedata["allonline"] = self.basedata["allonline"] + _online
            self.basedata["dayonline"] = self.basedata["dayonline"] + _online
            self.foronlinetime = time.time() * 1000  # 计算在线时间
            self.sendonline = time.time()
            await self.SendBasedata_bykey("dayonline", self.basedata["dayonline"])

    # 关闭连接
    async def close(self):
        self.logouttime = time.time() * 1000
        self.pobj.close()

    #初始化部分数据
    async def initInsertData(self):
        # 初始化玩家数据
        await self.DBM.initplayerdata(self.cid)

    async def SaveData(self):
        await self.DBM.Save_BaseData(self)
        await self.DBM.Save_signdata(self)
        await self.DBM.Save_timeseeddata(self)

    # 发送单个用户数据
    # ["cid"] = _data[0]
    # ["nick"] = _data[1]
    # ["sex"] = _data[2]
    # ["level"] = _data[3]
    # ["exp"] = _data[4]
    # ["gamemoney"] = _data[5]
    # ["paymoney"] = _data[6]
    # ["allonline"] = _data[7]
    # ["dayonline"] = _data[8]
    # ["logintime"] = _data[9]
    # ["logouttime"] = _data[10]
    async def SendBasedata_bykey(self, _key, _val):
        _data = {"key": _key, "val": _val}
        _msg = {"id": MsgDefine.USER_MSG_BASEDATA_KVAL, "mid": MsgDefine.BASEMSG, "data": _data}
        # print("SendBasedata_bykey", _msg)
        await self.ToClientMsg(_msg)

    # 接受消息
    async def ClientToServer(self, msg):
        # print(str(msg))
        try:
            _msg = json.loads(msg)
        except:
            print("json 解析报错！")
            return
        _msgid = int(_msg["id"])
        # print("ClientToServer__",_msgid,type(_msg["data"]),_msg["data"])
        if (_msgid == MsgDefine.MSG_HERTMSG):  # 心跳数据
            await self.client_Hertbeat()

        elif (_msgid == MsgDefine.USER_MSG_BUYSEED):  # 购买种子
            await self.client_buyseed(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT):  # 种植
            await self.client_plantnew(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_PICK):  # 植物状态按钮点击
            await self.client_plantpick(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_CHECK):  # 植物状态检测
            await self.client_plantcheckstate(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_CHANGESUIT):  # 换装备
            await self.client_changesuit(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_NEW):  # 开垦一个新的土地
            await self.client_newland(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_PLANT_HARVEST):  # 收获植物
            await self.client_harvest(_msg["data"])
        elif (_msgid == MsgDefine.USER_MSG_PLANT_SOLDSUIT):
            await self.client_soldsuit(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_TASKREWARD):  # 任务领取
            await self.client_taskreward(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_DOTASK):  # 做任务
            await self.client_dotask(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_ONLINEREWARD):  # 在线领取
            await self.client_onlinereward(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_LUCKYSTART):  # 开始抽奖
            await self.client_luckystart(_msg["data"])  #

        elif (_msgid == MsgDefine.USER_MSG_LUCKYREWARD):  # 幸运抽奖
            await self.client_luckyreward(_msg["data"])  #

        elif (_msgid == MsgDefine.USER_MSG_ACHIEVEAWARD):  # 成就领取奖励
            await self.client_achieveaward(_msg["data"])  #

        elif (_msgid == MsgDefine.USER_MSG_OPENSCENE):  # 开放场景
            await self.client_openscene(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_SAVESUIT):  # 保存套装数据
            await self.client_savesuit(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_THEMEMODELREWARD):  # 主题模特领取奖励
            await self.client_thememodere(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_SAVESUITACTION):  # 收藏界面保存套装数据操作
            await self.client_savesuitaction(_msg["data"])

        elif (_msgid == MsgDefine.USER_SHOPBUY):  # 商店购买
            await self.client_shopbuy(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_SIGN):  # 签到
            await self.client_sign(_msg["data"])

        elif (_msgid == MsgDefine.USER_MSG_FREESHOP):  # 免费商店
            await self.client_freeshop(_msg["data"])

        elif (_msgid == MsgDefine.USER_TIMESEED):  # 限时种子刷新
            await self.client_timesedupdate(_msg["data"])

        elif (_msgid == MsgDefine.USER_TIMESEEDBUY):  # 限时种子购买
            await self.client_buytimesed(_msg["data"])

        #  //

        elif (False):
            pass
        else:
            pass

    # 给客户端发送消息

    async def ToClientMsg(self, msg):
        # print(msg)
        _msg = json.dumps(msg)
        # print(_msg)
        # if(self.pobj.close)
        try:
            self.pobj.write_message(_msg)
        except:
            print("login out")

    async def SendToClientTips(self, id):
        _mgstr = ConfigData.GetMsgstr(id)
        _msg = {"id": id, "data": _mgstr}
        await self.To_C_Tips(_msg)

    async def To_C_Tips(self, msg):
        _msg = {"id": MsgDefine.GAME_MSG_TIPSMSG, "data": msg}
        await self.ToClientMsg(_msg)

    # **********************************************************
    # 客户端消息处理
    # **********************************************************

    # 心跳数据
    async def client_Hertbeat(self):
        self.herttime = time.time()
        # print("client_Hertbeat", self.herttime)
        await self.timersavedata()

    # 买种子
    async def client_buyseed(self, msg):
        _seedid = msg['seedid']
        _count = msg["count"]
        await self.C_buy_seed(_seedid, _count)

    # 种植土地
    async def client_plantnew(self, msg):
        index = int(msg['index'])
        seedid = msg["seedid"]
        await self.C_Plant_seed(index, seedid)

    # 土地状态点击
    async def client_plantpick(self, msg):
        index = int(msg['index'])
        _type = int(msg['type'])
        await self.C_Plant_pick(index, _type)

    # 检测土地状态
    async def client_plantcheckstate(self, msg):
        index = int(msg['index'])
        await self.C_Plant_check(index)

    #换装
    async def client_changesuit(self, msg):
        _id = int(msg['id'])
        await self.C_Suit_Change(_id)

    #开垦新的土地
    async def client_newland(self, msg):
        _id = int(msg['id'])
        await self.C_New_Plant(_id)

    # 收获
    async def client_harvest(self, msg):
        _id = int(msg['index'])
        _type = int(msg['type'])
        await self.C_Plant_Havest(_id, _type)

    # 出售衣服
    async def client_soldsuit(self, msg):
        _id = int(msg['id'])
        await self.C_Plant_soldsuit(_id)

    # 任务领取奖励
    async def client_taskreward(self, msg):
        _id = int(msg['id'])
        await self.C_task_reward(_id)

    # 做任务
    async def client_dotask(self, msg):
        _id = int(msg['id'])
        if (_id in [1011, 1010]):
            await self.do_task_id(_id)
            await self.checklasttask()

    # 在线领取奖励
    async def client_onlinereward(self, msg):
        _id = int(msg['id'])
        await self.C_online_reward(_id)

    # 开始抽奖
    async def client_luckystart(self, msg):
        _type = int(msg['type'])
        # print(_type)
        await self.C_Lucky_start(_type)

    # 幸运抽奖
    async def client_luckyreward(self, msg):
        _id = int(msg['id'])
        await self.C_Lucky_reward(_id)

    # 成就领取
    async def client_achieveaward(self, msg):
        _id = int(msg['id'])
        await self.C_achieve_award(_id)

    # 开放场景
    async def client_openscene(self, msg):
        _id = int(msg['id'])
        await self.C_openscene(_id)

    # 保存时装
    async def client_savesuit(self, msg):
        await self.C_savesuit()

    # 主题模特领取奖励
    async def client_thememodere(self, msg):
        _val = int(msg['val'])
        await self.C_thememodel_re(_val)
        pass

    # 保存套装数据操作类型
    async def client_savesuitaction(self, msg):
        _id = int(msg['id'])
        _type = int(msg['type'])
        await self.C_savesuitaction(_id, _type)
        pass

    # //商店购买
    async def client_shopbuy(self, msg):
        _type = int(msg['type'])
        if (_type == MsgDefine.USER_SHOPBUY_GIFT):
            _type = 1
        elif (_type == MsgDefine.USER_SHOPBUY_PAYMONEY):
            _type = 3
        elif (_type == MsgDefine.USER_SHOPBUY_GAMEMONEY):
            _type = 4
        _index = int(msg['index'])
        await self.C_shopbuy(_type, _index)
        pass

    # 签到
    async def client_sign(self, msg):
        await self.C_Sign()

    # 免费商店
    async def client_freeshop(self, msg):
        _index = int(msg['index'])
        await self.c_freeshop(_index)
        # raise NotImplementedError

    # 限时种子购买
    async def client_buytimesed(self, msg):
        _index = int(msg['index'])
        await self.client_buytimeseed(_index)

    # 限时种子数据刷新
    async def client_timesedupdate(self, msg):
        _index = int(msg['index'])
        await self.set_timeseeddata()
