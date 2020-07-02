import logging
import os
import os.path
import sys
import time

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d', time.localtime(time.time()))

_path = os.path.abspath('.')
log_path = os.path.dirname(_path) + '/mywebsocket/Logs/'
print(log_path)
# print(os.path.abspath(os.curdir))
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)


def info(log):
    logger.info(log)


def debug(log):
    logger.debug(log)


def warning(log):
    logger.warning(log)


def error(log):
    logger.error(log)


def critical(str):
    logger.critical(log)
