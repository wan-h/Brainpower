# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/

'''
Given a string, find the length of the longest substring without repeating characters.

Example 1:
Input: "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:
Input: "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
             Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(n)
    '''
    def lengthOfLongestSubstring(self, nums):
        dicts = {}
        maxlength = start = 0
        for index, num in enumerate(nums):
            if num in dicts:
                start = dicts[num] + 1
            maxcurr = index - start + 1
            maxlength = max(maxlength, maxcurr)
            dicts[num] = index
        return maxlength


if __name__ == '__main__':
    s = Solution()
    assert s.lengthOfLongestSubstring('abcabcbb') == 3
    assert s.lengthOfLongestSubstring('bbbbb') == 1
    assert s.lengthOfLongestSubstring('pwwkew') == 3

'''
intuition
分析题目可以得到用空间换取时间的解法，使用字典存储历史信息并查找，遍历一次完成求解。
'''