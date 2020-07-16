# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/excel-sheet-column-number/description/

'''
Given a column title as appear in an Excel sheet, return its corresponding column number.

For example:

    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28
    ...

Example 1:
Input: "A"
Output: 1


Example 2:
Input: "AB"
Output: 28


Example 3:
Input: "ZY"
Output: 701
'''

from functools import reduce

class Solution_1(object):
    def titleToNumber(self, s):
        return reduce(lambda x, y: x * 26 + y, [ord(c) - 64 for c in s])

class Solution_2(object):
    def titleToNumber(self, s):
        output = 0
        s = reversed(s)
        for exp, c in enumerate(s):
            output += (ord(c) - 64) * (26 ** exp)
        return output


if __name__ == '__main__':
    s1 = Solution_1()
    s2 = Solution_2()
    assert s1.titleToNumber('ZY') == 701
    assert s2.titleToNumber('ZY') == 701

'''
intuition
典型的多进制转换，解法二就是从经典的多进制转换算法出发，但是由于存在多次幂的大量重复计算
解法一则直接从取整累加的角度计算，相对来说计算量更小，可以类比在十进制里面384 = （3*10+8）*10 + 4
对于多进治制计算可以多参考十进制时候的通用接解法
'''