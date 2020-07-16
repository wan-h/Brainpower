# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/merge-sorted-array/description/

'''
Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.

Note:

The number of elements initialized in nums1 and nums2 are m and n respectively.
You may assume that nums1 has enough space (size that is greater or equal to m + n) to hold additional elements from nums2.
Example:

Input:
nums1 = [1,2,3,0,0,0], m = 3
nums2 = [2,5,6],       n = 3

Output: [1,2,2,3,5,6]
'''

class Solution(object):
    '''
    时间复杂度: O(n+m)
    空间复杂度: O(1)
    '''
    def merge(self, num1, m, num2, n):
        while m > 0 and n > 0:
            if num1[m - 1] <= num2[n - 1]:
                num1[m + n - 1] = num2[n - 1]
                n -= 1
            else:
                num1[m + n - 1] = num1[m - 1]
                m -= 1
        if n > 0:
            num1[: n] = num2[: n]

if __name__ == '__main__':
    s = Solution()
    num1 = [1, 2, 3, 0, 0, 0]
    m = 3
    num2 = [2, 5, 6]
    n = 3
    s.merge(num1, m, num2, n)
    assert num1 == [1, 2, 2, 3, 5, 6]

'''
intuition
两个有序序列进行比较，通过双指针法可以有效的节省空间，不同单独开辟空间来存储新的序列
'''