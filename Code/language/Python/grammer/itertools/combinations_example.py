# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import combinations, combinations_with_replacement

'''
combinations(iterable, r)
找出所有长度为r的排列情况
'''

test_list = [1, 2, 1]
print("=" * 21)
# 任意两个位置为元素都组合,且位置无先后关系，区别于全排列不考虑位置
for v in combinations(test_list, 2):
    print(f"Get combinations value: {v}")

print("=" * 21)
# 区别于combinations包含自生重复的情况，可以和自己组合
for v in combinations_with_replacement(test_list, 2):
    print(f"Get combinations value: {v}")