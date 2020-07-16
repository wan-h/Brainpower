# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/top-k-frequent-elements/solution/description/

'''
Given a non-empty array of integers, return the k most frequent elements.

Example 1:
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:
Input: nums = [1], k = 1
Output: [1]

Note:
You may assume k is always valid, 1 ≤ k ≤ number of unique elements.
Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
'''

import collections
import heapq

class Solution(object):
    '''
    时间复杂度: O(nlog(n))
    空间复杂度: O(n)
    '''
    def topKFrequent(self, nums, k):
        count = collections.Counter(nums)
        return heapq.nlargest(k, count.keys(), key=count.get)

if __name__ == '__main__':
    s = Solution()
    assert s.topKFrequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]

'''
intuition
熟悉python的内建包，成为有利的工具
'''