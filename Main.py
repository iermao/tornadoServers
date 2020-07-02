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


if __name__ == '__main__':
    app()
