# import json

# aaa = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# # print(aaa)

# print(type(aaa))

# aaastr = str(aaa)

# print(aaastr)

# print(type(aaastr))

# bb = eval(aaastr)

# print(bb)

# print(type(bb))

# # aaastr = aaastr.replace("'", '"')

# # cc = json.loads(aaastr)

# # print(cc)

# # print(type(bb))
# # bb = aaastr.split(',')

# # print(bb)

# # print(type(aaastr.split(',')))

# # aaalist = list(aaastr)
# # print(aaalist)

# # print(type(aaalist))

import os

import datetime
import time

# str = ('python main.py IC.txt')

# p = os.system(str)

now_time = datetime.datetime.now()

print(now_time)

string = str(now_time)

# time1 = datetime.datetime.strptime(string,'%M')

time.localtime().tm_hour

print(time.localtime().tm_min)

print(time.localtime().tm_sec)
