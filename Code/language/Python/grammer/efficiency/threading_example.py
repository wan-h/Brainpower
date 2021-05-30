# coding: utf-8
# Author: wanhui0729@gmail.com

'''
python多线程受GIL限制，适合解决I/O密集型问题
'''

import time
import threading
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

'''
Thread创建多线程
'''
def run(name='Python'):
    for _ in range(2):
        print(f"hello, {name}")
        time.sleep(1)

def example_1():
    thread1 = Thread(target=run)
    # 开始执行
    thread1.start()
    thread2 = Thread(target=run, args=('Golang',))
    thread2.start()
    thread3 = Thread(target=run, kwargs={'name': 'C++'})
    thread3.start()
    # 等待线程执行结束
    thread1.join()
    thread2.join()
    thread3.join()
    print("Thread创建多线程完成")

'''
使用类创建多线程
'''
class MyThread(Thread):
    def __init__(self, name='Python'):
        super().__init__()
        self.name = name
    def run(self):
        for _ in range(2):
            print(f"Hello, {self.name}")
            time.sleep(1)
def example_2():
    thread1 = MyThread()
    thread1.start()
    thread2 = MyThread('Golang')
    thread2.start()
    thread1.join()
    thread2.join()
    print("使用类创建多线程完成")

'''
threading相关函数
'''
def example_3():
    t = Thread(target=run)
    # 设置线程名
    t.name = "My-Thread"
    # 设置线程是否随主线程退出而退出，默认为False
    t.daemon = True
    # 启动子线程
    t.start()
    # 判断线程是否在执行状态，在执行返回True，否则返回False
    print("running state:", t.is_alive())
    # 阻塞子线程，待子线程结束后，再往下执行
    t.join()

'''
线程锁
'''
def job1():
    global n, lock
    with lock:
        for i in range(10):
            n += 1
            print('job1', n)
def job2():
    global n, lock
    with lock:
        for i in range(10):
            n += 10
            print('job2', n)
n = 0
lock = threading.Lock()
def example_4():
    thread1 = Thread(target=job1)
    thread2 = Thread(target=job2)
    thread1.start()
    thread2.start()

'''
线程池
'''
def target():
    for i in range(5):
        print('running thread-{}:{}'.format(threading.get_ident(), i))
        time.sleep(1)
def example_5():
    #: 生成线程池最大线程为5个
    pool = ThreadPoolExecutor(5)
    for _ in range(100):
        pool.submit(target)  # 往线程中提交，并运行

if __name__ == '__main__':
    # example_1()
    # example_2()
    # example_3()
    # example_4()
    example_5()