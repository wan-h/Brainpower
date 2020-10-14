# coding: utf-8
# Author: wanhui0729@gmail.com

'''
构建装饰器函数
常用场景：
1. 授权
2. 日志
'''

from functools import wraps

def my_wraps(func):
    @wraps(func)
    def wrapTheFunc(*args, **kwargs):
        print("I am doing something before excuting func")
        func(*args, **kwargs)
        print("I am doing something after excuting func")
    return wrapTheFunc

class MyWrapsClass(object):
    '''
    可以实现一个装饰器的基类，然后用于其他定制装饰器的继承
    '''
    def __init__(self, debug=True):
        self.debug = debug

    def __call__(self, func):
        @wraps(func)
        def wrapTheFunc(*args, **kwargs):
            log_string = func.__name__ + " was called" + f", args: {args}" + f", kwargs: {kwargs}."
            if self.debug:
                print(log_string)
            return func(*args, **kwargs)
        return wrapTheFunc

@my_wraps
def func_1(a, b=2):
    print(f"Get Value: {a+b}")

@MyWrapsClass()
def func_2(a, b=2):
    res = a + b
    print(f"Get Value: {a + b}")
    return res

if __name__ == '__main__':
    func_1(3)
    print("*" * 10)
    res = func_2(2, b=1)