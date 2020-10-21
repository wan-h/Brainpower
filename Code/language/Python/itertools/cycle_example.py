# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import cycle

'''
循环返回一个可迭代对象
'''

c = cycle('ABC')
tag = 0
for v in c:
    print(f"Get cycle value: {v}")
    tag += 1
    if tag > 10: break
