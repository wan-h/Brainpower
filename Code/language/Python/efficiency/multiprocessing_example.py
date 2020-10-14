# coding: utf-8
# Author: wanhui0729@gmail.com

'''
适合解决cpu密集型问题
'''

from multiprocessing import Process, Pool, Queue
import os
import time
import random

'''
multiprocessing创建多进程
很多用法类似threading
'''

def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

def example_1():
    print('Parent child process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test', ))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')

# 进程池
def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

def example_2():
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    # 最后一个要等到前面有一个结束之后才开始执行，因为池大小只有4
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    # 不能再添加新的process
    p.close()
    # 等待子进程执行结束
    p.join()
    print('All subprocesses done.')

# 进程间通信
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

def example_3():
    q = Queue()
    pw = Process(target=write, args=(q, ))
    pr = Process(target=read, args=(q, ))
    pw.start()
    pr.start()
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()


if __name__ == '__main__':
    # example_1()
    # example_2()
    example_3()