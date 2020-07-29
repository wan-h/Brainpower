# coding: utf-8
# Author: wanhui0729@gmail.com

'''
协程具有程极高的执行效率。
子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。
不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

Python对协程的支持是通过generator实现的。
在generator中，我们不但可以通过for循环来迭代，还可以不断调用next()函数获取由yield语句返回的下一个值。
但是Python的yield不但可以返回一个值，它还可以接收调用者发出的参数。
'''

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    # 启动生成器
    c.send(None)
    n = 0
    while n < 5:
        n += 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return %s' % r)
    c.close()

def example_1():
    c = consumer()
    produce(c)

# 实现并发
'''
Python 3.4版本引入的标准库asyncio, 内置了对异步IO的支持
'''

import threading
import asyncio

# 装饰器定义函数为协程类型
@asyncio.coroutine
def hello_1():
    print('Hello world! (%s)' % threading.current_thread())
    # asyncio.sleep(1)也是协程，所以主线程不会等待，去执行其他可以执行的coroutine了，因此可以实现并发执行。
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.current_thread())

def example_2():
    loop = asyncio.get_event_loop()
    tasks = [hello_1(), hello_1()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

# 为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。
async def hello_2():
    print('Hello world! (%s)' % threading.current_thread())
    await asyncio.sleep(1)
    print('Hello again! (%s)' % threading.current_thread())

def example_3():
    loop = asyncio.get_event_loop()
    tasks = [hello_2(), hello_2()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

# 最高效率，多进程+协程，gevent和进程池存在冲突，不建议一起使用
import gevent
import requests
from multiprocessing import Process
# 需要阻塞时自动切换协程
from gevent import monkey; monkey.patch_all()
def fetch(url):
    try:
        s = requests.Session()
        r = s.get(url, timeout=1)
    except Exception as e:
        print(e)
    return ''

def process_start(url_list):
    tasks = []
    for url in url_list:
        tasks.append(gevent.spawn(fetch, url))
    # 使用协程执行
    gevent.joinall(tasks)

def example_4():
    url_list = []
    for i in range(1000):
        url_list.append('https://www.baidu.com')
        if i % 100 == 0:
            p = Process(target=process_start, args=(url_list,))
            p.start()
            url_list = []
    if url_list is not []:  # 若退出循环后任务队列里还有url剩余
        p = Process(target=process_start, args=(url_list,))  # 把剩余的url全都放到最后这个进程来执行
        p.start()


if __name__ == '__main__':
    # example_1()
    # example_2()
    # example_3()
    example_4()