# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import zip_longest

'''
zip_longest(iter1 [,iter2 [...]], [fillvalue=None])
和zip类似，不同地方在于:
zip结束取决于里面最短的迭代对象
zip_longest结束取决于里面最长的迭代对象
'''

print("=" * 21)
print("zip iter:")
# 按照最短的元素做组合操作
for x, y in zip([1, 2, 3], [1, 2]):
    print(x, y)

print("=" * 21)
print("ziplongest iter:")
# 按照最短长的元素做组合操作, 没有的位置使用None补齐
for x, y in zip_longest([1, 2, 3], [1, 2]):
    print(x, y)