
# 数据库管理
# import os

# import json
# import datetime

# import logging
# import sys

import pymysql
from tornado_mysql import pools


class DBHelper():
    POOL = pools.Pool(dict(host='127.0.0.1',
                           port=3306,
                           user='root',
                           passwd='root',
                           db='gardendressup',charset='utf8'),
                      max_idle_connections=1,
                      max_recycle_sec=3)

    def __init__(self, _host="127.0.0.1", _port=3306, _user="root", _password="root", _database="gardendressup"):
        pass
        # print("DBHelper   __init__")
        # self.host = _host
        # self.port = _port
        # self.user = _user
        # self.pwd = _password
        # self.db = _database

        # self.conn = None
        # self.cur = None

        # self.connectDatabase()
    # # 数据库连接
    # def connectDatabase(self):
    #     try:
    #         self.conn = pymysql.connect(self.host, self.user, self.pwd, self.db, charset="utf8")
    #         self.conn.autocommit(1)
    #         self.cur = self.conn.cursor()
    #     except():
    #         print("db connect err")
    #         return False
    #     finally:
    #         pass
    #         # print("1")
    #     return True

    # # 数据库关闭
    # def close(self):
    #     if self.conn and self.cur:
    #         self.cur.close()
    #         self.conn.close()
    #     return True

    # 数据库操作---插入数据
    async def execute(self, sql, params  =  None):
        cur = await self.POOL.execute(sql)# self.cur.execute(sql, params)
        return True

    # 插入一条语句返回自增id
    async def getinsertdata_id(self, sql):
        cur = await self.POOL.execute(sql) #self.cur.execute(sql)
        last_id = self.cur.lastrowid
        return last_id

    #查询返回结果
    async def Seldata(self,sql):
        cur = await self.POOL.execute(sql)
        return cur.fetchone()


    
