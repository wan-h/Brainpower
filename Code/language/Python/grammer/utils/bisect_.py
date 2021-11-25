# coding: utf-8
# Author: wanhui0729@gmail.com

'''
二分搜索
'''

import bisect
import random

HAYSTACK = [1, 4, 5,  6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]

ROW_FMT = '{0:2d} @ {1:2d}    {2}{0:<2d}'

def demo(bisect_fn):
    for needle in reversed(NEEDLES):
        position = bisect_fn(HAYSTACK, needle)
        offset = position * '  |'
        print(ROW_FMT.format(needle, position, offset))

# bisect_left
print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
demo(bisect.bisect_left)

# bisect_right
print('=' * 21)
print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
demo(bisect.bisect_right)

# insort
print('=' * 21)
SIZE = 7
random.seed(1729)

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE * 2)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)