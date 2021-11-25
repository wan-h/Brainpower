# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import islice

'''
islice(iterable, stop)
islice(iterable, start, stop[, step])
这个就是对迭代对象进行切割，不支持负数，类似于切片操作
'''

test_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# islice(test_list, 2, 6, 2) 等价于 test_list[2: 6: 2]
for v in islice(test_list, 2, 6, 2):
    print(f"Get islice value: {v}")