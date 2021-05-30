# coding: utf-8
# Author: wanhui0729@gmail.com

'''
定时器实现
'''

import time
import sched
from datetime import datetime
from threading import Timer

'''
使用threading模块定时器
'''
def threading_timer(inc):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # time.sleep(3) 执行时间会和延时时间叠加
    # Timer三个参数分别为：间隔时间、被调用触发的函数，给该触发函数的参数（tuple形式)
    t = Timer(inc, threading_timer, (inc, ))
    t.start()

if __name__ == '__main__':
    threading_timer(2)

'''
使用sched模块
'''
# 初始化sched模块的 scheduler 类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)
# 被周期性调度触发的函数
def sched_timer(inc):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # time.sleep(3) 执行时间会和延时时间叠加
    # enter四个参数分别为：间隔时间、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，给该触发函数的参数（tuple形式)
    schedule.enter(inc, 0, sched_timer, (inc, ))

if __name__ == '__main__':
    schedule.enter(0, 0, sched_timer, (2, ))
    schedule.run()