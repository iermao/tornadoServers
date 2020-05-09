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
    def selUser(self, _name, _pwd):
        sql = "select Max(id) from `userdata` where `uid` = '{0}' and `pwd` = '{1}' "
        sql = sql.format(_name, _pwd)
        _data = self.dbhelper.Seldata(sql)
        # print(_data)
        return _data[0]

    #初始化数据
    def initplayerdata(self, cid):

        sql = "select cid from `player` where `cid` = '{0}'"
        sql = sql.format(cid)
        _data = self.dbhelper.Seldata(sql)
        print(_data)
        if (_data == None):
            sql = "insert into `player` ( `cid`,`createtime`,`logintime`,`logouttime`,`nick`,`sex`,`level`,`exp`,`gamemoney`,`paymoney`,`suitdata`,`dressdata`,`plantdata`,`seeddata`) values ({0},{1},{2},{3},'',1,1,1,0,0,'','','','');"
            _time = time.time() * 1000
            sql = sql.format(cid, _time, _time, _time)
            self.dbhelper.execute(sql)

    #获得玩家基础数据
    def getBaseData(self, cid):
        sql = "select `cid`,`nick`,`sex`,`level`,`exp`,`gamemoney`,`paymoney`,`suitdata`,`dressdata`,`plantdata`,`seeddata` from `player` where cid = {0}"
        sql = sql.format(cid)
        _data = self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            _list["nick"] = _data[1]
            _list["sex"] = _data[2]
            _list["level"] = _data[3]
            _list["exp"] = _data[4]
            _list["gamemoney"] = _data[5]
            _list["paymoney"] = _data[6]
        return _list

    # 获得玩家换装以及获得的装备
    def getHomeData(self, cid):
        sql = "select `cid`,`suitdata`,`dressdata` from `player` where cid = {0}"
        sql = sql.format(cid)
        _data = self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]

            _list["suitdata"] = self.initSuitData(_data[1])

            _list["dressdata"] = self.initDressData(_data[2])

        return _list

    # 农场种植数据以及种子数据
    def getSeedAndPlantData(self, cid):
        sql = "select `cid`,`plantdata`,`seeddata` from `player` where cid = {0}"
        sql = sql.format(cid)
        _data = self.dbhelper.Seldata(sql)
        _list = {}
        if (_data != None):
            _list["cid"] = _data[0]
            _list["plantdata"] = self.initPlantData(_data[1])
            _list["seeddata"] = self.initSeedData(_data[2])
        return _list

    # 初始化---当前穿搭数据
    def initSuitData(self, _data):
        if (_data == ""):
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            return eval(_data)

    # 初始化---当前衣服物品数据
    def initDressData(self, _data):
        if (_data == ""):
            return [10101]
        else:
            return eval(_data)

    # 初始化植物数据
    def initPlantData(self, _data):
        if (_data == ""):
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
        if (_data == ""):
            return {"10001": 10}
        else:
            return eval(_data)

    #保存玩家基础数据
    def Save_BaseData(self, _puser):

        sql = "UPDATE `player` set `logintime` = {0},  `logouttime` = {1}, `level` = {2},  `exp` = {3},  `gamemoney` = {4},  `paymoney` = {5}  where cid = {6} ;"
        sql = sql.format(_puser.logintime, _puser.logouttime, _puser.basedata["level"], _puser.basedata["exp"], _puser.basedata["gamemoney"], _puser.basedata["paymoney"], _puser.cid)
        self.dbhelper.execute(sql)

    def Save_homedata(self, _puser):
        sql = "UPDATE `player` set `suitdata` = '{0}',  `dressdata` = '{1}' where cid = {2} ;"

        _suitdata = str(_puser.suitdata)
        _dressdata = str(_puser.dressdata)

        sql = sql.format(_suitdata, _dressdata, _puser.cid)
        self.dbhelper.execute(sql)

    def Save_farmdata(self, _puser):
        sql = "UPDATE `player` set `plantdata` = '{0}',  `seeddata` = '{1}' where cid = {2} ;"

        _plantdata = json.dumps(_puser.plantdata)
        _seeddata = json.dumps(_puser.seeddata)

        sql = sql.format(_plantdata, _seeddata, _puser.cid)
        self.dbhelper.execute(sql)
        pass