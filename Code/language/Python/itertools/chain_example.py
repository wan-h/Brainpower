# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import chain

'''
chain: 可以接受多个迭代对象
chain.from_iterable():可以接受一个可以产生迭代对象的迭代器
'''

def chain_example():
    # 字典只获取key
    ch = chain([1, 2], {'3': 3}, {4, '5'}, (6,), ['7', [8, '9']])
    print("=" * 21)
    for v in ch:
        print(f"Get chain value: {v}")

def chain_from_iterable():
    def gen_iterables():
        for i in range(5):
            yield range(i)
    print("=" * 21)
    # 对迭代器所有返回迭代对象使用chain
    for v in chain.from_iterable(gen_iterables()):
        print(f"Get chain value: {v}")

if __name__ == '__main__':
    chain_example()
    chain_from_iterable()