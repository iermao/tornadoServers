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
        sql = "select `cid`,`suitdata`,`seeddata` from `player` where cid = {0}"
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
            return []
        else:
            return eval(_data)

    # 初始化植物数据
    def initPlantData(self, _data):
        if (_data == ""):
            return {
                "0": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "3": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
            return {}
        else:
            return eval(_data)
