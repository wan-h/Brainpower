# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/factorial-trailing-zeroes/description/

'''
Given an integer n, return the number of trailing zeroes in n!.

Example 1:

Input: 3
Output: 0
Explanation: 3! = 6, no trailing zero.
Example 2:

Input: 5
Output: 1
Explanation: 5! = 120, one trailing zero.
Note: Your solution should be in logarithmic time complexity.
'''

class Solution_1(object):
    '''
    递归
    时间复杂度: O(logn)
    空间复杂度: O(logn)
    '''
    def trailingZeroes(self, n):
        if n == 0: return 0
        return n // 5 + self.trailingZeroes(n // 5)

class Solution_2(object):
    '''
    因式分解
    时间复杂度: O(logn)
    空间复杂度: O(1)
    '''
    def trailingZeroes(self, n):
        count = 0
        while n >= 5:
            n = n // 5
            count += n
        return count

if __name__ == '__main__':
    s1 = Solution_1()
    s2 = Solution_2()
    assert s1.trailingZeroes(1) == 0
    assert s1.trailingZeroes(5) == 1
    assert s2.trailingZeroes(1) == 0
    assert s2.trailingZeroes(5) == 1

'''
intuition
分析问题只需要得出再做阶乘可以因式分解成多少个5即可
以上两种方法在本质上没有任何区别，只是递归再代码上更容易理解，精简
'''