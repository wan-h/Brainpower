# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/power-of-four/description/

'''
Given an integer (signed 32 bits), write a function to check whether it is a power of 4.

Example 1:
Input: 16
Output: true

Example 2:
Input: 5
Output: false

Follow up: Could you solve it without loops/recursion?
'''

class Solution(object):
    '''
    时间复杂度: O(1)
    空间复杂度: O(1)
    '''
    def isPowerOfFour(self, num):
        if num == 0: return True
        if num & (num - 1) == 0 and num & 0x55555555 == num:
            return True
        else:
            return False

if __name__ == '__main__':
    s = Solution()
    assert s.isPowerOfFour(16)
    assert not s.isPowerOfFour(5)

'''
intuition
转换为二进制后观察二进制的分布规则找到解题思路
'''