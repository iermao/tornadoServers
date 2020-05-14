#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Runner for testing autoreload module."""

import os, time

from autoreload import run_with_reloader


def runner():
    print("[%s]enter..." % os.getpid())
    while 1:
        time.sleep(1)
    print("[%s]runner." % os.getpid())


if __name__ == '__main__':

    run_with_reloader(runner)