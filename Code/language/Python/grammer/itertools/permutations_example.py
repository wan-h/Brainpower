# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import permutations

'''
permutations(iterable[, r])
全排列，输出迭代对象所有可能的排列
'''

# 只和位置有关系，和元素取值没有关系
test_list = [1, 2, 1]
print("=" * 21)
for v in permutations(test_list):
    print(f"Get permutations value: {v}")

# 任意两个位置为元素都组合,且位置有先后关系
print("=" * 21)
for v in permutations(test_list, 2):
    print(f"Get permutations value: {v}")