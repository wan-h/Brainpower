# coding: utf-8
# Author: wanhui0729@gmail.com

'''
调用任务
'''

import time
from proj.task import add, mul
from celery.app.control import Control
from proj.celery import app
from celery.result import AsyncResult

# 获取app队列信息
queue_info = app.connection().channel().queue_declare('proj', passive=True)
print('message count:', queue_info.message_count)
# 清空队列
app.connection().channel().queue_purge('proj')


result = add.delay(4, 4)
# 获取task id
print("task id: ", str(result.id))
# 获取task对象
task = AsyncResult(str(result.id))
# 获取task状态,进入开始执行状态
time.sleep(1)
print("task status: ", task.status)

celery_control = Control(app=app)
# 属于强制终止，后台会有报错信息
celery_control.revoke(str(result.id), terminate=True, signal='SIGKILL')
# 进入任务撤销状态
time.sleep(1)
print("task done: ", task.status)

# 同步阻塞等待结果
# print("result: ", result.get(timeout=1))
#
# 参数签名
s1 = mul.s(2, 2)
res = s1.delay()
print("signature result: ", res.get())