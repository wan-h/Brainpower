# coding: utf-8
# Author: wanhui0729@gmail.com

from __future__ import absolute_import

from .celery import app

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y
