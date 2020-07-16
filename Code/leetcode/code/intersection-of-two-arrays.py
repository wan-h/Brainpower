# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/intersection-of-two-arrays/description/

'''
Given two arrays, write a function to compute their intersection.

Example 1:
Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2]

Example 2:
Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [9,4]

Note:
Each element in the result must be unique.
The result can be in any order.
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def intersection(self, nums1, nums2):
        return set(nums1) & set(nums2)


if __name__ == '__main__':
    s = Solution()
    assert s.intersection([4, 9, 5], [9, 4, 9, 8, 4]) == {9, 4}

'''
intuition
正常思路通过hash存储,每个list遍历一遍即可求解
也可利用python的语言特性,用set快速求解
'''