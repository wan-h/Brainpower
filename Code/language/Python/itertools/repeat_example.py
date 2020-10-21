# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import repeat

'''
重复返回一个对象指定次数
'''

repeat_number = 5
r = repeat(1, repeat_number)
for v in r:
    print(f"Get cycle value: {v}")
