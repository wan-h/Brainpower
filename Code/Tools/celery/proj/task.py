# coding: utf-8
# Author: wanhui0729@gmail.com

from __future__ import absolute_import
import time
from .celery import app

@app.task
def add(x, y):
    try:
        # 模拟耗时
        time.sleep(10)
        return x + y
    except:
        pass

@app.task
def mul(x, y):
    return x * y
