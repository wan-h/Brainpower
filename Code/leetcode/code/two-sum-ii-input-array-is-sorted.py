# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/

'''
Given an array of integers that is already sorted in ascending order, find two numbers such that they add up to a specific target number.

The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2.

Note:

Your returned answers (both index1 and index2) are not zero-based.
You may assume that each input would have exactly one solution and you may not use the same element twice.
Example:

Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore index1 = 1, index2 = 2.
'''
class Solution_1(object):
    '''
    双指针法
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def twoSum(self, numbers, target):
        left, right = 0, len(numbers) - 1
        while left < right:
            if numbers[left] + numbers[right] > target:
                right -= 1
            if numbers[left] + numbers[right] < target:
                left += 1
            if numbers[left] + numbers[right] == target:
                return [left+1, right+1]

class Solution_2(object):
    '''
    空间换取时间
    时间复杂度: O(n)
    空间复杂度: O(n)
    '''
    def twoSum(self, numbers, target):
        visited = {}
        for index, number in enumerate(numbers):
            if target - number in visited:
                return [visited[target - number], index + 1]
            else:
                visited[number] = index + 1

if __name__ == '__main__':
    s1 = Solution_1()
    s2 = Solution_2()
    assert s1.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert s2.twoSum([2, 7, 11, 15], 9) == [1, 2]

'''
intuition
常见处理方法可以想到使用空间换取时间的方法，但是没有利用到已排序的特性
双指针法则很好的利用了排序的特性且将空间复杂度降到最低
'''