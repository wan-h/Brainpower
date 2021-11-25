# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import accumulate

'''
使用func的函数对迭代对象进行累积
'''

test_list = [i for i in range(5)]
for v in accumulate(test_list, lambda x, y: x + y):
    print(f"Get accumulate value: {v}")
