# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import product

'''
product(*iterables, repeat=1)
相当于迭代器之间各个元素做排列组合
'''

print("=" * 21)
for i, j in product([1, 2, 3], [1, 2]):
    print(i, j)

print("=" * 21)
# 使用repeat表示对迭代元素的重复使用的排列组合
for i, j in product([1, 2], repeat=2):
    print(i, j)