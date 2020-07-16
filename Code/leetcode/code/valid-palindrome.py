# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/valid-palindrome/description/

'''
Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

Note: For the purpose of this problem, we define empty string as valid palindrome.

Example 1:

Input: "A man, a plan, a canal: Panama"
Output: true
Example 2:

Input: "race a car"
Output: false
'''

class Solution_1(object):
    '''
    双指针法
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def isPalindrome(self, s):
        left, right = 0, len(s) - 1
        while left < right:
            if not s[left].isalnum():
                left += 1
                continue
            if not s[right].isalnum():
                right -= 1
                continue
            if s[left].lower() == s[right].lower():
                left += 1
                right -= 1
            else:
                break
        return right <= left

class Solution_2(object):
    '''
    利用语言特性
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def isPalindrome(self, s):
        s = [*filter(str.isalnum, s.lower())]
        return s == s[::-1]

if __name__ == '__main__':
    s1 = Solution_1()
    s2 = Solution_2()
    assert s1.isPalindrome("A man, a plan, a canal: Panama")
    assert s2.isPalindrome("A man, a plan, a canal: Panama")
    assert s1.isPalindrome("race a car") is False
    assert s2.isPalindrome("race a car") is False

'''
intuition
首位字符比较有序符合双指针的策略
另外通过python的语言特性可以可以使用简单的代码对问题进行求解
'''