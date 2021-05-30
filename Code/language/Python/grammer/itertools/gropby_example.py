# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import groupby

'''
groupby(iterable, key=None)
对字符串，列表等进行分组(迭代对象的相同元素分到一组)
'''

# 对字符串进行分组，将相同字符的分到一组
print("=" * 21)
print("Group by str")
for k, g in groupby('11111223'):
    print(k, list(g))

# 按照字典的value进行分组
test_dict = {
    '1': 1,
    '2': 1,
    '3': 2
}
print("=" * 21)
print("Group by dict value")
for k, g in groupby(test_dict, lambda x: test_dict.get(x)):
  print(k, list(g))
