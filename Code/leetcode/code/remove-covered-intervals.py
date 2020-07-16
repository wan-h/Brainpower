# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/remove-covered-intervals/

'''
Given a list of intervals, remove all intervals that are covered by another interval in the list.
Interval [a,b) is covered by interval [c,d) if and only if c <= a and b <= d.
After doing so, return the number of remaining intervals.

Example 1:
    Input: intervals = [[1,4],[3,6],[2,8]]
    Output: 2
    Explanation: Interval [3,6] is covered by [2,8], therefore it is removed.

Constraints:
* 1 <= intervals.length <= 1000
* 0 <= intervals[i][0] < intervals[i][1] <= 10^5
* intervals[i] != intervals[j] for all i != j
'''

class Solution(object):
    '''
    动态规划转换方程：dp[i] = max(dp[i - 2] + nums[i - 2], dp[i - 1])
    时间复杂度: O(nlogn)
    空间复杂度: O(1)
    '''
    def removeCoveredIntervals(self, intervals: list):
        # Sort by start point.
        # If two intervals share the same start point
        # put the longer one to be the first.
        intervals.sort(key=lambda x: (x[0], -x[1]))
        count = 0
        prev_end = 0
        for _, end in intervals:
            if end > prev_end:
                count += 1
                prev_end = end
        return count

if __name__ == '__main__':
    s = Solution()
    assert s.removeCoveredIntervals([[1, 4], [3, 6], [2, 8]]) == 2

'''
intuition
贪心算法先将全局最优解问题转化一个通过局部最优解获得全局最优解的问题，然后求解局部最优解
'''