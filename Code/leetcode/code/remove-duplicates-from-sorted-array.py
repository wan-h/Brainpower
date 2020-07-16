# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/

'''
Given a sorted array nums, remove the duplicates in-place such that each element appear only once and return the new length.

Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra memory.

Example 1:

Given nums = [1,1,2],

Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively.

It doesn't matter what you leave beyond the returned length. Example 2:

Given nums = [0,0,1,1,1,2,2,3,3,4],

Your function should return length = 5, with the first five elements of nums being modified to 0, 1, 2, 3, and 4 respectively.

It doesn't matter what values are set beyond the returned length. Clarification:

Confused why the returned value is an integer but your answer is an array?

Note that the input array is passed in by reference, which means modification to the input array will be known to the caller as well.

Internally you can think of this:
    // nums is passed in by reference. (i.e., without making a copy)
    int len = removeDuplicates(nums);

    // any modification to nums in your function would be known by the caller.
    // using the length returned by your function, it prints the first len elements.
    for (int i = 0; i < len; i++) {
        print(nums[i]);
    }
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def removeDuplicates(self, nums):
        if nums:
            slow = 0
            for fast in range(1, len(nums)):
                if nums[fast] != nums[slow]:
                    slow += 1
                    nums[slow] = nums[fast]
            return (slow + 1)
        return 0

if __name__ == '__main__':
    s = Solution()
    check_list1 = [1, 1, 2]
    check_list1_ret = s.removeDuplicates(check_list1)
    assert check_list1_ret == 2
    assert check_list1[:check_list1_ret] == [1, 2]

    check_list2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    check_list2_ret = s.removeDuplicates(check_list2)
    assert check_list2_ret == 5
    assert check_list2[:check_list2_ret] == [0, 1, 2, 3, 4]

'''
intuition
双指针法，因为数据是有序的，所有这种两两比较存在一定的规律，通过快慢指针可以进行有规律的比较
从而降低时间复杂度和空间复杂度（双指针只需要额外存储另一个指针的空间）
'''