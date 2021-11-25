# coding: utf-8
# Author: wanhui0729@gmail.com

from functools import lru_cache

'''
lru_cache 用于函数缓存，在连续用相同参数调用一个函数时，函数使用存储值作为返回值
接受maxsize和typed两个参数
maxsize为缓存最多maxsize个此函数的结果
typed为是否对参数类型敏感，例如设置为True时，f(3)和f(3.0)会被分别存储
'''

@lru_cache(maxsize=2)
def add(x, y):
    print(f"calculating: {x} + {y}")
    return x+y

if __name__ == '__main__':
    # 存储第一个
    add(1, 2)
    add(1, 2)
    add(1, 2)
    # 存储第二个
    add(2, 3)
    add(2, 3)
    # 存储第三个，maxsize为２,覆盖掉最先存储的
    add(3, 4)
    # 已经被覆盖掉，重新调用函数计算
    add(1, 2)