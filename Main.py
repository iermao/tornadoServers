# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

from Server.app import app
import os
import sys
import time
import atexit
import signal
import traceback


def term_sig_handler(signum, frame):
    print('catched singal: {}'.format(signum))
    sys.exit()


@atexit.register
def atexit_fun():
    print('i am exit, stack track:')

    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, term_sig_handler)
    signal.signal(signal.SIGTERM, term_sig_handler)

    print('start arg 1:', str(sys.argv))
    print("run  in  {}".format(os.getpid()))
    if (str(sys.argv[1]) == "start"):
        app()
