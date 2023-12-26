import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

Executor = ThreadPoolExecutor(max_workers=12)

async def async_executor(func, *args, **kwargs):
    """构建异步执行器: 线程池中执行传入函数 """
    loop = asyncio.get_event_loop()
    # 实际上这里使用一个线程池来维护了多个函数的执行
    result = await loop.run_in_executor(Executor, func, *args, **kwargs)
    return result

async def fun1():
    print("[fun1] in")
    await async_executor(time.sleep, 1)
    print("[fun1] out")

async def fun2():
    print("[fun2] in")
    await async_executor(time.sleep, 2)
    print("[fun2] out")

async def fun3():
    print("[fun3] in")
    await async_executor(time.sleep, 3)
    print("[fun3] out")

async def fun4():
    print("[fun4] in")
    await async_executor(time.sleep, 1)
    print("[fun4] out")

async def main():
    print("[main] in")
    task1 = asyncio.create_task(fun1())
    task2 = asyncio.create_task(fun2())
    task3 = asyncio.create_task(fun3())
    # 上面3个已经被加入任务队列，所以已经可以被协程调度执行
    print("[main] tasks created")
    # 这里等待了task1执行完成,所有task4是要等到task1的结果才可以执行的
    # 说白了,await就是等待异步函数返回结果
    # 这里的await就相当于控制权交会给了事件循环,然后事件循环就去执行循环队列中的任务,直到这个异步返回结果
    await task1
    task4 = asyncio.create_task(fun4())
    await task2
    await task3
    await task4
    print("[main] out")


if __name__ == '__main__':
    asyncio.run(main())