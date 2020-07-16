# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/subsets/description/

'''
Given a set of distinct integers, nums, return all possible subsets (the power set).

Note: The solution set must not contain duplicate subsets.

Example:

Input: nums = [1,2,3]
Output:
[
  [3],
  [1],
  [2],
  [1,2,3],
  [1,3],
  [2,3],
  [1,2],
  []
]
'''

class Solution(object):
    '''
    双指针法
    时间复杂度: O(n*2^n)
    空间复杂度: O(2^n)
    '''
    def subsets(self, nums):
        output = [[]]
        for num in nums:
            output += [curr + [num] for curr in output]
        return output

if __name__ == '__main__':
    s = Solution()
    assert s.subsets([1, 2, 3]) == [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

'''
intuition
排列组合的实现，可以用用于相关的需要暴力计算的排列组合上面
'''