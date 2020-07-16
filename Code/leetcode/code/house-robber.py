# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/house-robber/description/

'''
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight without alerting the police.

Example 1:

Input: [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
             Total amount you can rob = 1 + 3 = 4.
Example 2:

Input: [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
             Total amount you can rob = 2 + 9 + 1 = 12.
'''

class Solution(object):
    '''
    动态规划转换方程：dp[i] = max(dp[i - 2] + nums[i - 2], dp[i - 1])
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def rob(self, nums):
        if not nums:
            return 0
        prevMax = 0
        currMax = 0
        for num in nums:
            currMax, prevMax = max(prevMax + num, currMax), currMax
        return currMax


if __name__ == '__main__':
    s = Solution()
    assert s.rob([1, 2, 3, 1]) == 4
    assert s.rob([2, 7, 9, 3, 1]) == 12

'''
intuition
a, b = b, a利用python的语言特性可以更加高效的编程
动态规划的重点是找到转换方程和初始值，然后迭代更新中间状态就可以了
'''