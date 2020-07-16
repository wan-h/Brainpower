# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/product-of-array-except-self/description/

'''
Given an array nums of n integers where n > 1,  return an array output such that output[i] is equal to the product of
all the elements of nums except nums[i].

Example:
Input:  [1,2,3,4]
Output: [24,12,8,6]

Note: Please solve it without division and in O(n).

Follow up:
Could you solve it with constant space complexity? (The output array does not count as extra space for the purpose of
space complexity analysis.)
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(n)
    '''
    def productExceptSelf(self, nums):
        length = len(nums)
        answers = [0] * length
        answers[0] = 1

        for i in range(1, length):
            answers[i] = answers[i - 1] * nums[i - 1]

        R = 1
        for i in reversed(range(length)):
            answers[i] = answers[i] * R
            R *= nums[i]

        return answers

if __name__ == '__main__':
    s = Solution()
    assert s.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]


'''
intuition
通过图解可以进一步分析问题
Lanswer[i] = answer[i - 1] * num[i - 1]
Ranswer[i] = answer[i + 1] * num[i + 1]
answer[i] = Lanswer[i] * Ranswer[i]

在遇到有规律的问题时，可以通过图解进一步分析问题解法
'''