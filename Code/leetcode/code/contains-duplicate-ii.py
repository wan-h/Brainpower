# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/contains-duplicate-ii/description/

'''
Given an array of integers and an integer k, find out whether there are two distinct indices i and j in the array such that nums[i] = nums[j] and the absolute difference between i and j is at most k.

Example 1:

Input: nums = [1,2,3,1], k = 3
Output: true
Example 2:

Input: nums = [1,0,1,1], k = 1
Output: true
Example 3:

Input: nums = [1,2,3,1,2,3], k = 2
Output: false
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(n)
    '''
    def containsNearbyDuplicate(self, nums, k):
        d = {}
        for index, num in enumerate(nums):
            if num in d and index - d[num] <= k:
                return True
            d[num] = index
        return False

if __name__ == '__main__':
    s = Solution()
    assert s.containsNearbyDuplicate([1, 2, 3, 1], 3) == True
    assert s.containsNearbyDuplicate([1, 0, 1, 1], 1) == True
    assert s.containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2) == False

'''
intuition
使用字典用空间换取时间
'''