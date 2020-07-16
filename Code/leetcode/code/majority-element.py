# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/majority-element/description/

'''
Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always exist in the array.

Example 1:

Input: [3,2,3]
Output: 3
Example 2:

Input: [2,2,1,1,1,2,2]
Output: 2
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def majorityElement(self, nums):
        count, majority = 1, nums[0]
        for num in nums[1:]:
            if count == 0:
                majority = num
            if num == majority:
                count += 1
            else:
                count -= 1
        return majority

if __name__ == '__main__':
    s = Solution()
    assert s.majorityElement([3, 2, 3]) == 3
    assert s.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2

'''
intuition
可以使用空间换取时间的方法，但是这样就缺少了对条件more than ⌊ n/2 ⌋的使用，且空间复杂度高
分析问题使用投票算法，只保存当前最多个数的元素来反复投票获得投票最高的元素
'''