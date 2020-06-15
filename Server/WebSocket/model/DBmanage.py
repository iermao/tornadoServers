import os, json
import time
import pymysql
import logging
import sys

from .DBHelper import DBHelper


# 数据管理
class dbmanage():
    def __init__(self):
        self.dbhelper = DBHelper()
        pass

    # #注册一个新用户
    # def NewUserData(self, name, pwd):
    #     _addtime = time.time() * 1000
    #     name = 123
    #     pwd = "1111111111"
    #     sql = "insert into `userdata` (`addtime`,`uid`,`pwd`,`logintime`) values ({0},{1},{2},{3});"
    #     sql = sql.format(_addtime, name, pwd, _addtime)
    #     print("sql   " + str(sql))
    #     _id = self.dbhelper.getinsertdata_id(sql)
    #     print("NewUserData   " + str(_id))

    #查询用户名是否被注册
    async def selUser(self, _name, _pwd):
        sql = "select Max(id) from `userdata` where `uid` = '{0}' and `pwd` = '{1}' "
        sql = sql.format(_name, _pwd)
        _data = await self.dbhelper.Seldata(sql)
        # print(_data)
        return _data[0]

    # ************************************************************************
    # 读取数据---from  mysql
    # 开始
    # ************************************************************************

    #初始化数据

    async def initplayerdata(self, cid):

        # 初始化玩家数据表
        sql = "select cid from `player` where `cid` = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        # print(_data)
        if (_data == None):
            sql = "insert into `player` ( `cid`,`createtime`,`logintime`,`logouttime`,`nick`,`sex`,`level`,`exp`,`gamemoney`,`paymoney`,`signdata`,`guidesta`) values ({0},{1},{2},{3},'',1,1,1,2000,1000,'',0);"
            _time = time.time() * 1000
            sql = sql.format(cid, _time, _time, _time)
            await self.dbhelper.execute(sql)

        # 初始衣服表
        _table = "player_dressdata"
        sql = "select cid from `{0}` where `cid` = {1}"
        sql = sql.format(_table, cid)
        _data = await self.dbhelper.Seldata(sql)
        if (_data == None):
            sql = "insert into `{0}` ( `cid`,`suitdata`,`dressdata`) values ({1},'{2}','{3}');"
            sql = sql.format(_table, cid, '', '')
            await self.dbhelper.execute(sql)

        # 初始农场表
        _table = "player_farmdata"
        sql = "select cid from `{0}` where `cid` = {1}"
        sql = sql.format(_table, cid)
        _data = await self.dbhelper.Seldata(sql)
        if (_data == None):
            sql = "insert into `{0}` ( `cid`,`plantdata`,`seeddata`) values ({1},'{2}','{3}');"
            sql = sql.format(_table, cid, '', '')
            await self.dbhelper.execute(sql)

        # 初始化任务表
        _table = "player_taskdata"
        sql = "select cid from `{0}` where `cid` = {1}"
        sql = sql.format(_table, cid)
        _data = await self.dbhelper.Seldata(sql)
        if (_data == None):
            sql = "insert into `{0}` ( `cid`,`data`,`dayonlinerew`) values ({1},'{2}','{3}');"
            sql = sql.format(_table, cid, '', '')
            await self.dbhelper.execute(sql)

        # 初始化成就表
        _table = "player_achievedata"
        sql = "select cid from `{0}` where `cid` = {1}"
        sql = sql.format(_table, cid)
        _data = await self.dbhelper.Seldata(sql)
        if (_data == None):
            sql = "insert into `{0}` ( `cid`,`data`) values ({1},'{2}');"
            sql = sql.format(_table, cid, '')
            await self.dbhelper.execute(sql)

        # 初始化所有种植植物数据表
        _table = "player_plantdata"
        sql = "select cid from `{0}` where `cid` = {1}"
        sql = sql.format(_table, cid)
        _data = await self.dbhelper.Seldata(sql)
        if (_data == None):
            sql = "insert into `{0}` ( `cid`,`data`) values ({1},'{2}');"
            sql = sql.format(_table, cid, '')
            await self.dbhelper.execute(sql)

        # 初始化保存的套装数据
        _table = "player_savesuitdata"
        sql = "select cid from `{0}` where `cid` = {1}"
        sql = sql.format(_table, cid)
        _data = await self.dbhelper.Seldata(sql)
        if (_data == None):
            sql = "insert into `{0}` ( `cid`,`data`) values ({1},'{2}');"
            sql = sql.format(_table, cid, '')
            await self.dbhelper.execute(sql)

        # 初始化限时种子数据
        _table = "player_timeseedbuy"
        sql = "select cid from `{0}` where `cid` = {1}"
        sql = sql.format(_table, cid)
        _data = await self.dbhelper.Seldata(sql)
        if (_data == None):
            sql = "insert into `{0}` ( `cid`,`timeseeddata`) values ({1},'{2}');"
            sql = sql.format(_table, cid, '')
            await self.dbhelper.execute(sql)

    #获得玩家基础数据
    async def getBaseData(self, cid):
        sql = "select `cid`,`nick`,`sex`,`level`,`exp`,`gamemoney`,`paymoney`,`allonline`,`dayonline`,`logintime`,`logouttime`,`lucktime`,`guidesta` from `player` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            _list["nick"] = _data[1]
            _list["sex"] = _data[2]
            _list["level"] = _data[3]
            _list["exp"] = _data[4]
            _list["gamemoney"] = _data[5]
            _list["paymoney"] = _data[6]
            _list["allonline"] = _data[7]
            _list["dayonline"] = _data[8]
            _list["logintime"] = _data[9]
            _list["logouttime"] = _data[10]
            _list["lucktime"] = _data[11]
            if (_data[12] == None):
                _list["guidesta"] = 0
            else:
                _list["guidesta"] = _data[12]
        return _list

    # 获取签到数据
    async def getsigndata(self, cid):
        sql = "select `cid`,`signdata` from `player` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            if (_data[1] != "" and _data[1] != None):
                _tmpdata = eval(_data[1])
                if (len(_tmpdata) < 1):
                    _list["signdata"] = {}
                else:
                    _list["signdata"] = _tmpdata
            else:
                _list["signdata"] = {}

        return _list

    # 获取限时购买种子数据
    async def get_freeseeddata(self, cid):
        sql = "select `cid`,`timeseeddata` from `player_timeseedbuy` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            if (_data[1] != "" and _data[1] != None):
                _tmpdata = eval(_data[1])
                if (len(_tmpdata) < 1):
                    _list["timeseeddata"] = {"0": [], "1": []}
                else:
                    _list["timeseeddata"] = _tmpdata
            else:
                _list["timeseeddata"] = {"0": [], "1": []}

        return _list

    # 获得玩家换装以及获得的装备
    async def getHomeData(self, cid):
        sql = "select `cid`,`suitdata`,`dressdata` ,`suitlist` from `player_dressdata` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]

            # 当前穿戴数据
            _list["suitdata"] = self.initSuitData(_data[1])
            # 拥有衣服数据
            _list["dressdata"] = self.initDressData(_data[2])

            # 获取在线数据
            if (_data[3] != "" and _data[3] != None):
                _tmpdata = eval(_data[3])
                if (len(_tmpdata) < 1):
                    _list["suitlist"] = {}
                else:
                    _list["suitlist"] = _tmpdata
            else:
                _list["suitlist"] = {}

        return _list

    # 获得 农场种植数据以及种子数据
    async def getSeedAndPlantData(self, cid):
        sql = "select `cid`,`plantdata`,`seeddata` from `player_farmdata` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            _list["plantdata"] = self.initPlantData(_data[1])
            _list["seeddata"] = self.initSeedData(_data[2])
        return _list

    # 获取所有种植过的植物数据
    async def getallplantdata(self, cid):
        sql = "select `cid`,`data` from `player_plantdata` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            if (_data[1] != ""):
                _list["data"] = eval(_data[1])
            else:
                _list["data"] = {}
        return _list

    # 获得玩家任务数据
    async def gettaskdata(self, cid):
        sql = "select `cid`,`data`,`dayonlinerew`,`openscene` from `player_taskdata` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            if (_data[1] != ""):
                _list["data"] = eval(_data[1])
            else:
                _list["data"] = {}

            # 获取在线数据
            if (_data[2] != "" and _data[2] != None):
                _tmpdata = eval(_data[2])
                if (len(_tmpdata) < 1):
                    _list["dayonlinerew"] = []
                else:
                    _list["dayonlinerew"] = _tmpdata
            else:
                _list["dayonlinerew"] = []

            # 获取场景数据
            print(_data[3])
            if (_data[3] != "" and _data[3] != None):
                _tmpdata = eval(_data[3])
                if (len(_tmpdata) < 1):
                    _list["openscene"] = []
                else:
                    _list["openscene"] = _tmpdata
            else:
                _list["openscene"] = []

        return _list

    # 获得玩家成就数据
    async def getachievedata(self, cid):
        sql = "select `cid`,`data` from `player_achievedata` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            if (_data[1] != ""):
                _list["data"] = eval(_data[1])
            else:
                _list["data"] = {}
        return _list

    # 获得玩家保存的套装数据
    async def getsavesuitdata(self, cid):
        sql = "select `cid`,`data` from `player_savesuitdata` where cid = {0}"
        sql = sql.format(cid)
        _data = await self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            if (_data[1] != ""):
                _list["data"] = eval(_data[1])
            else:
                _list["data"] = []
        return _list

    # ************************************************************************
    # 读取数据---from  mysql
    # 结束
    # ************************************************************************

    # ************************************************************************
    # 初始化数据库读取数据
    # 开始
    # ************************************************************************

    # 初始化---当前穿搭数据
    def initSuitData(self, _data):
        if (str(_data).replace(' ', '') == ""):
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            return eval(_data)

    # 初始化---当前衣服物品数据
    def initDressData(self, _data):
        if (str(_data).replace(' ', '') == ""):
            return []
        else:
            return eval(_data)

    # 初始化植物数据
    def initPlantData(self, _data):
        if (str(_data).replace(' ', '') == ""):
            return {
                "0": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "1": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "2": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "3": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "4": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "5": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "6": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "7": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        else:
            return eval(_data)

    # 初始化种子数据
    def initSeedData(self, _data):
        if (str(_data).replace(' ', '') == ""):
            return {"1001": 10}
        else:
            return eval(_data)

    # ************************************************************************
    # 初始化数据库读取数据
    # 结束
    # ************************************************************************

    # ************************************************************************
    # 保存数据
    # 开始
    # ************************************************************************

    #保存玩家基础数据
    async def Save_BaseData(self, _puser):
        sql = "UPDATE `player` set `logintime` = {0},  `logouttime` = {1}, `level` = {2},  `exp` = {3},  `gamemoney` = {4},  `paymoney` = {5},  `allonline` = {7},  `dayonline` = {8},  `lucktime` = {9},  `guidesta` = {10}  where cid = {6} ;"
        sql = sql.format(_puser.logintime, _puser.logouttime, _puser.basedata["level"], _puser.basedata["exp"], _puser.basedata["gamemoney"], _puser.basedata["paymoney"], _puser.cid, _puser.basedata["allonline"], _puser.basedata["dayonline"], _puser.basedata["lucktime"], _puser.basedata["guidesta"])

        # print(sql)
        await self.dbhelper.execute(sql)

    # 保存签到数据
    async def Save_signdata(self, _puser):
        sql = "UPDATE `player` set `signdata` = '{0}'  where cid = {1} ;"
        _signdata = json.dumps(_puser.signdata)
        sql = sql.format(_signdata, _puser.cid)
        await self.dbhelper.execute(sql)

    # 保存衣服以及当前穿戴数据
    async def Save_homedata(self, _puser):
        sql = "UPDATE `player_dressdata` set `suitdata` = '{0}',  `dressdata` = '{1}',  `suitlist` = '{3}' where cid = {2} ;"

        _suitdata = str(_puser.suitdata)
        _dressdata = str(_puser.dressdata)
        _suitlistdata = json.dumps(_puser.suitlist)

        sql = sql.format(_suitdata, _dressdata, _puser.cid, _suitlistdata)
        await self.dbhelper.execute(sql)

    # 保存农场以及种子数据
    async def Save_farmdata(self, _puser):
        sql = "UPDATE `player_farmdata` set `plantdata` = '{0}',  `seeddata` = '{1}' where cid = {2} ;"

        _plantdata = json.dumps(_puser.plantdata)
        _seeddata = json.dumps(_puser.seeddata)

        sql = sql.format(_plantdata, _seeddata, _puser.cid)
        await self.dbhelper.execute(sql)
        pass

    # 保存任务数据
    async def Save_taskdata(self, _puser):
        sql = "UPDATE `player_taskdata` set `data` = '{0}', `dayonlinerew` = '{2}', `openscene` = '{3}'  where cid = {1} ;"
        _data = json.dumps(_puser.taskdata)
        _dayonlinerewdata = json.dumps(_puser.dayonlinerew)
        _openscene = json.dumps(_puser.openscene)
        sql = sql.format(_data, _puser.cid, _dayonlinerewdata, _openscene)
        await self.dbhelper.execute(sql)
        pass

    # 保存成就数据
    async def Save_achievedata(self, _puser):
        sql = "UPDATE `player_achievedata` set `data` = '{0}' where cid = {1} ;"
        _data = json.dumps(_puser.achievedata)
        sql = sql.format(_data, _puser.cid)
        await self.dbhelper.execute(sql)
        pass

    # 保存所有植物数据
    async def save_allplantdata(self, _puser):
        sql = "UPDATE `player_plantdata` set `data` = '{0}' where cid = {1} ;"
        _data = json.dumps(_puser.allplantdata)
        sql = sql.format(_data, _puser.cid)
        await self.dbhelper.execute(sql)
        pass

    # 保存保存的套装数据
    async def Save_savesuitdata(self, _puser):
        sql = "UPDATE `player_savesuitdata` set `data` = '{0}' where cid = {1} ;"
        _data = json.dumps(_puser.savesuit)
        sql = sql.format(_data, _puser.cid)
        await self.dbhelper.execute(sql)
        pass

    # 保存限时种子数据
    async def Save_timeseeddata(self, _puser):
        sql = "UPDATE `player_timeseedbuy` set `timeseeddata` = '{0}' where cid = {1} ;"
        _data = json.dumps(_puser.timeseeddata)
        sql = sql.format(_data, _puser.cid)
        await self.dbhelper.execute(sql)
        pass

    # ************************************************************************
    # 保存数据
    # 结束
    # ************************************************************************

    # ************************************************************************
    # log数据
    # 开始
    # ************************************************************************
    async def log_plant(self, _puser, plantindex, sedid, table):
        sql = "insert into `{0}` (`createtime`,`cid`,`plantindex`,`seedid`) values ({1},{2},{3},{4});"
        _time = 0
        _time = int(round(time.time() * 1000))  #time.time()
        sql = sql.format(table, _time, _puser.cid, plantindex, sedid)
        try:
            await self.dbhelper.execute(sql)
        except Exception as e:
            print("log err " + str(e))
            return False

    # ************************************************************************
    # log数据
    # 结束
    # ************************************************************************
