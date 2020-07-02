from tornado.ioloop import IOLoop
from tornado import gen
import tormysql

from Server import config

import time

pool = tormysql.helpers.ConnectionPool(
    max_connections=20,
    idle_seconds=7200,
    wait_connection_timeout=3,
    # host='localhost',
    # port=3306,
    # user='root',
    # passwd='A@111111a',
    # db='mysql',
    # charset='utf8',
    host=config.web_mysql_ip,
    port=config.web_mysql_point,
    user=config.web_mysql_user,
    passwd=config.web_mysql_passwd,
    db=config.web_mysql_db,
    charset=config.web_mysql_charset)


# 查询用户uid---用户注册的时候使用
async def Seluid(uid):

    sql = "SELECT `id` FROM userdata  where uid = '" + uid + "' LIMIT 1"
    cur = await pool.execute(sql)
    aaaaa = -1
    try:
        aaaaa = cur.fetchone()[0]
    except:
        aaaaa = -1
    return aaaaa


# 用户登录查询
async def SelUser(uid, pwd):
    sql = "SELECT `id` FROM userdata  where uid = '" + uid + "' and pwd = '" + pwd + "' LIMIT 1"
    cur = await pool.execute(sql)
    aaaaa = -1
    try:
        aaaaa = cur.fetchone()[0]
    except:
        aaaaa = -1

    return aaaaa


# 注册用户
async def RegUser(uid, pwd):
    _addtime = time.time() * 1000

    sql = "insert into `userdata` (`addtime`,`uid`,`pwd`,`logintime`) values ({0},'{1}','{2}',{3})"
    sql = sql.format(_addtime, uid, pwd, _addtime)

    cur = await pool.execute(sql)
    aaaaa = cur.lastrowid
    return aaaaa


ioloop = IOLoop.instance()