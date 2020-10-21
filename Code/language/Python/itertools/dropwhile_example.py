# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import dropwhile

'''
dropwhile(predicate, iterable)
循环开始的条件是直到遇到第一次不满足pred条件的情况，才开始遍历
'''

# 4开始不满足条件
test_list = [1, 2, 4, 2, 5, 8]
for v in dropwhile(lambda x: x < 3, test_list):
    print(f"Get dropwhile value: {v}")