import json
import time
import hashlib

import tornado.web
from tornado import gen

from . import dbhelper


class Account():
    def __init__(self):
        print("__init__  Account")
        pass

    async def Reg(self, _data, http):
        _jsondtaa = json.loads(_data)
        _cmd = _jsondtaa["cmd"]
        _name = _jsondtaa["name"]
        _pwd = _jsondtaa["pwd"]

        _pwdmd5 = hashlib.md5(_pwd.encode(encoding='UTF-8')).hexdigest()
        msg = {'code': -1, 'msg': '', 'uid': '', 'pwd': '', 'keys': ''}
        _tmpstr = (_name + "wowadmin+=-09").encode(encoding='UTF-8')
        _key = hashlib.md5(_tmpstr).hexdigest()

        if (_cmd == "login"):
            _seluid = await dbhelper.SelUser(_name, _pwdmd5)
            # print("login", _seluid, msg)
            if (_seluid > 0):
                msg = self.GetMsg(0, "ok")
            else:
                msg = self.GetMsg(1, "no reg")
        elif (_cmd == "reg"):
            _seluid = await dbhelper.Seluid(_name)
            if (_seluid > 0):
                msg = self.GetMsg(1, "account have reg")
            else:
                _seluid = await dbhelper.RegUser(_name, _pwdmd5)
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

    # 统一返回消息
    def GetMsg(self, code, errmsg):
        msg = {'code': -1, 'msg': '', 'uid': '', 'pwd': '', 'keys': ''}
        msg["code"] = code
        msg["msg"] = errmsg
        return msg
