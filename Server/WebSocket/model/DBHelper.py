
# 数据库管理
# import os

# import json
# import datetime

# import logging
# import sys
import pymysql

class DBHelper():
    def __init__(self, _host="127.0.0.1", _port=3306, _user="root", _password="root", _database="gardendressup"):
        # print("DBHelper   __init__")
        self.host = _host
        self.port = _port
        self.user = _user
        self.pwd = _password
        self.db = _database

        self.conn = None
        self.cur = None

        self.connectDatabase()
    # 数据库连接

    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(self.host, self.user, self.pwd, self.db, charset="utf8")
            self.conn.autocommit(1)
            self.cur = self.conn.cursor()
        except():
            print("db connect err")
            return False
        finally:
            pass
            # print("1")
        return True

    # 数据库关闭
    def close(self):
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 数据库操作---插入数据
    def execute(self, sql, params  =  None):
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()
        except:
            print("execute error,{0}".format(str(sql)))
            return False
        return True

    # 插入一条语句返回自增id
    def getinsertdata_id(self, sql):
        self.cur.execute(sql)
        last_id = self.cur.lastrowid
        return last_id

    #查询返回结果
    def Seldata(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchone()


    
