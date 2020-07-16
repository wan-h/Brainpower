# coding: utf-8
# Author: wanhui0729@gmail.com

# Link：https://leetcode.com/problems/maximum-subarray/

'''
Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

Example:

Input: [-2,1,-3,4,-1,2,1,-5,4],
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.
Follow up:

If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
'''

import sys

class Solution_1(object):
    '''
    分治法
    把数组nums以中间位置（m)分为左（left)右(right)两部分. 那么有， left = nums[0]...nums[m - 1] 和 right = nums[m + 1]...nums[n-1]
    最大子序列和的位置有以下三种情况：
        1.考虑中间元素nums[m], 跨越左右两部分，这里从中间元素开始，往左求出后缀最大，往右求出前缀最大, 保持连续性。
        2.不考虑中间元素，最大子序列和出现在左半部分，递归求解左边部分最大子序列和
        3.不考虑中间元素，最大子序列和出现在右半部分，递归求解右边部分最大子序列和
    时间复杂度: O(nlogn)
    空间复杂度: O(logn)
    '''
    def maxSubArray(self, nums):
        return self.helper(nums, 0, len(nums) - 1)
    def helper(self, nums, l, r):
        if l > r:
            return -sys.maxsize
        mid = (l + r) // 2
        left = self.helper(nums, 1, mid - 1)
        right = self.helper(nums, mid + 1, r)
        left_suffix_max_sum = right_prefix_max_sum = 0
        sum = 0
        for i in reversed(range(0, mid)):
            sum += nums[i]
            left_suffix_max_sum = max(left_suffix_max_sum, sum)
        sum = 0
        for i in range(mid + 1, r + 1):
            sum += nums[i]
            right_prefix_max_sum = max(right_prefix_max_sum, sum)
        cross_max_sum = left_suffix_max_sum + right_prefix_max_sum + nums[mid]
        return max(cross_max_sum, left, right)

class Solution_2(object):
    '''
    动态规划
    dp[i]表示到当前位置i的最大子序列和
    状态转移方程为： dp[i] = max(dp[i - 1] + nums[i], nums[i])
    初始化：dp[0] = nums[0]
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def maxSubArray(self, nums):
        n = len(nums)
        max_sum_ending_curr_index = max_sum = nums[0]
        for i in range(1, n):
            max_sum_ending_curr_index = max(max_sum_ending_curr_index + nums[i], nums[i])
            max_sum = max(max_sum_ending_curr_index, max_sum)
        return max_sum

class Solution_3(object):
    '''
    优化前缀法
    定义函数 S(i)，它的功能是计算以0（包括0）开始加到i（包括 i）的值。
    那么S(j)-S(i-1)就等于从i开始（包括i）加到j（包括j）的值。
    因此只需要用一个变量来维护最小值，一个变量维护最大值就可以求解一个点是否大值解。
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def maxSubArray(self, nums):
        n = len(nums)
        maxSum = nums[0]
        minSum = sum = 0
        for i in range(n):
            sum += nums[i]
            maxSum = max(maxSum, sum - minSum)
            minSum = min(minSum, sum)
        return maxSum

if __name__ == '__main__':
    s1 = Solution_1()
    s2 = Solution_2()
    s3 = Solution_3()
    assert s1.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert s2.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert s3.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

'''
intuition
从不同的角度看问题有不同的解法，从子序列中间元素看是看引出分治法
从子序列最后一个元素看引出动态规划
优化前缀法通过仔细分析问题，用简答的代码实现了动态规划的低复杂度
'''