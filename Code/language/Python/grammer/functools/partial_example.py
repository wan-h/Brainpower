# coding: utf-8
# Author: wanhui0729@gmail.com

'''
partial填充函数参数并返回一个新的函数
'''

from functools import partial

def cal(a, b, c):
    return a - b + c

cal_func1 = partial(cal, 1)
cal_func2 = partial(cal, 3, 1)

if __name__ == '__main__':
    print(f"cal_fun1 result: {cal_func1(1, 3)} ==> 1 - 1 + 3")
    print(f"cal_fun2 result: {cal_func2(2)} ==> 3 - 1 + 2")