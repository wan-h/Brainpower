# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import compress

'''
compress(data, selectors)
根据selectors的bool判断新的迭代器是否获得对应位置的元素
(d[0] if s[0]), (d[1] if s[1]), ...
'''

data = ['A', 'B', 'C', 'D']
# 只有对应位置的'B','D'被选择
selectors = [0, 1, 0, 1]
for v in compress(data, selectors):
    print(f"Get compress value: {v}")