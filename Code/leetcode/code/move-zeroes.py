# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/move-zeroes/description/

'''
Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Example:

Input: [0,1,0,3,12]
Output: [1,3,12,0,0]
Note:

You must do this in-place without making a copy of the array.
Minimize the total number of operations.
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def moveZeroes(self, nums):
        fast = slow = 0
        while fast < len(nums):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1
            fast += 1


if __name__ == '__main__':
    s = Solution()
    nums = [0, 1, 0, 3, 12]
    s.moveZeroes(nums)
    assert nums == [1, 3, 12, 0, 0]

'''
intuition
使用双指针的方法做inplace操作可以尽可能的减少空间复杂度
快慢指针位置交换的操作可以实现移位的思想
'''