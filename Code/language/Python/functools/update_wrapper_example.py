# coding: utf-8
# Author: wanhui0729@gmail.com

import functools as ft

'''
弥补函数经过wraper或partial操作后的属性改变
'''

def hi(func):
    def wrapper():
        "Hi has taken over Hello Documentation"
        print("Hi geeks")
        func()
    return wrapper

@hi
def hello():
    "this is the documentation of Hello Function"
    print("Hey Geeks")

# hello函数的相关属性已经被修改
print(hello.__name__)
print(hello.__doc__)
help(hello)


def new_hi(func):
    def wrapper():
        "Hi has taken over Hello Documentation"
        print("Hi geeks")
        func()

    print("UPDATED WRAPPER DATA")
    # 模型拷贝了原函数中的 {ft.WRAPPER_ASSIGNMENTS} 属性作为更新
    print(f'WRAPPER ASSIGNMENTS : {ft.WRAPPER_ASSIGNMENTS}')
    # 将要被重新更新的属性，默认__dict__就是更新所有属性
    print(f'UPDATES : {ft.WRAPPER_UPDATES}')

    ft.update_wrapper(wrapper, func)
    return wrapper

@new_hi
def hello():
    "this is the documentation of Hello Function"
    print("Hey Geeks")

# hello相关的函数属性并未被改变
print(hello.__name__)
print(hello.__doc__)
help(hello)
