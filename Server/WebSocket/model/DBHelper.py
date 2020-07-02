# 数据库管理
# import os

# import json
# import datetime

# import logging
# import sys

import pymysql
from tornado_mysql import pools

from Server import config


class DBHelper():
    POOL = pools.Pool(dict(host=config.ws_mysql_ip, port=config.ws_mysql_point, user=config.ws_mysql_user, passwd=config.ws_mysql_passwd, db=config.ws_mysql_db, charset=config.ws_mysql_charset), max_idle_connections=1, max_recycle_sec=3)

    def __init__(self):
        pass

    # 数据库操作---插入数据
    async def execute(self, sql, params=None):
        cur = await self.POOL.execute(sql)  # self.cur.execute(sql, params)
        return True

    # 插入一条语句返回自增id
    async def getinsertdata_id(self, sql):
        cur = await self.POOL.execute(sql)  #self.cur.execute(sql)
        last_id = self.cur.lastrowid
        return last_id

    #查询返回结果
    async def Seldata(self, sql):
        cur = await self.POOL.execute(sql)
        return cur.fetchone()
