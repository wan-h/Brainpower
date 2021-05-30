# coding: utf-8
# Author: wanhui0729@gmail.com

from itertools import count

'''
def count(firstval=0, step=1):
        x = firstval
        while 1:
            yield x
            x += step
'''

start = 1
step = 2
c = count(start, step)
for v in c:
    print(f"Get count value: {v}")
    if v > 10: break

