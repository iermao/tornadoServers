# #################
# CFun.py 常用函数库
# iermao
# #################
#!/usr/bin/python
# -*- coding: UTF-8 -*-


def filter_url(_str):
    _str = str(_str)
    _str = _str.replace(' ', '')
    _str = _str.replace(';', '')
    _str = _str.replace("'", "")
    _str = _str.replace('"', '')
    return _str
