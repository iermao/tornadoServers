import json
import time
import hashlib
import Server.WebSocket.model.DBHelper

import tornado.web
from tornado import gen
# import tornado_mysql
from tornado_mysql import pools


class Account():
    POOL = pools.Pool(dict(host='127.0.0.1',
                           port=3306,
                           user='root',
                           passwd='root',
                           db='gardendressup'),
                      max_idle_connections=1,
                      max_recycle_sec=3)

    def __init__(self):
        pass

    async def Reg(self, _data, http):
        # print("reg")
        _jsondtaa = json.loads(_data)
        _cmd = _jsondtaa["cmd"]
        _name = _jsondtaa["name"]
        _pwd = _jsondtaa["pwd"]
        # if (_name == "a111111"):
        #     await gen.sleep(10)

        _pwdmd5 = hashlib.md5(_pwd.encode(encoding='UTF-8')).hexdigest()
        msg = {'code': -1, 'msg': '', 'uid': '', 'pwd': '', 'keys': ''}
        _tmpstr = (_name + "wowadmin+=-09").encode(encoding='UTF-8')
        _key = hashlib.md5(_tmpstr).hexdigest()

        if (_cmd == "login"):
            _seluid = await self.SelUser(_name, _pwdmd5)
            print(_seluid)
            if (_seluid > 0):
                msg = self.GetMsg(0, "ok")
            else:
                msg = self.GetMsg(1, "no reg")

        elif (_cmd == "reg"):
            _seluid = await self.Seluid(_name)
            if (_seluid > 0):
                msg = self.GetMsg(1, "account have reg")
            else:
                _seluid = await self.RegUser(_name, _pwdmd5)
                if (_seluid > 0):
                    msg = self.GetMsg(0, "reg ok")
                else:
                    msg = self.GetMsg(2, "reg err")
        else:
            msg = self.GetMsg(99, "other err")

        msg["uid"] = str(_name)
        msg["pwd"] = str(_pwdmd5)
        msg["keys"] = str(_key)

        msg = json.dumps(msg)
        return msg
        # raise gen.Return(msg)
        # msg = json.dumps(msg)
        # print(msg)
        # http.finish()
        # http.write(msg)

    # 查询用户uid---用户注册的时候使用
    @gen.coroutine
    async def Seluid(self, uid):
        sql = "SELECT `id` FROM userdata  where uid = '" + uid + "' LIMIT 1"

        cur = await self.POOL.execute(sql)

        aaaaa = -1
        try:
            aaaaa = cur.fetchone()[0]
        except:
            aaaaa = -1
        # raise gen.Return(aaaaa)
        return aaaaa

    # 用户登录查询
    # @gen.coroutine
    async def SelUser(self, uid, pwd):
        sql = "SELECT `id` FROM userdata  where uid = '" + uid + "' and pwd = '" + pwd + "' LIMIT 1"

        cur = await self.POOL.execute(sql)

        aaaaa = -1
        try:
            aaaaa = cur.fetchone()[0]
        except:
            aaaaa = -1
        # raise gen.Return(aaaaa)
        return aaaaa

    # 注册用户
    # @gen.coroutine
    async def RegUser(self, uid, pwd):
        _addtime = time.time() * 1000
        sql = "insert into `userdata` (`addtime`,`uid`,`pwd`,`logintime`) values ({0},'{1}','{2}',{3})"
        sql = sql.format(_addtime, uid, pwd, _addtime)
        cur = await self.POOL.execute(sql)

        aaaaa = cur.lastrowid
        print(aaaaa)
        # aaaaa = -1
        # if (_oneobj != None):
        #     aaaaa = cur.fetchone()[0]
        #     print(aaaaa)

        # raise gen.Return(aaaaa)
        return aaaaa

    # 统一返回消息
    def GetMsg(self, code, errmsg):
        msg = {'code': -1, 'msg': '', 'uid': '', 'pwd': '', 'keys': ''}
        msg["code"] = code
        msg["msg"] = errmsg
        return msg
