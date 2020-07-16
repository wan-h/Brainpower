# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/single-number/description/

'''
Given a non-empty array of integers, every element appears twice except for one. Find that single one.

Note:

Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?
'''

class Solution(object):
    '''
    双指针法
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def singleNumber(self, nums):
        single_number = 0
        for num in nums:
            single_number ^= num
        return single_number

if __name__ == '__main__':
    s = Solution()
    assert s.singleNumber([4, 1, 2, 1, 2]) == 4

'''
intuition
通过二进制异或的特性求解问题
异或可以解决和序列顺序无关的对对碰问题
'''