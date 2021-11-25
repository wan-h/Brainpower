# coding: utf-8
# Author: wanhui0729@gmail.com

from functools import reduce

'''
reduce对可迭代对象执行滚雪球操作
'''

a = [1, 2, 3]
b = reduce(lambda x, y: x+y, a)
print(f"列表a的累和为{b}=> 1 + 2 + 3")
c = reduce(lambda x, y: x+y, a, 4)
print(f"列表a初始化为4的累和为{c}=> 4 + 1 + 2 + 3")