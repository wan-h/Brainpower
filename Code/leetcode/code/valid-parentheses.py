# coding: utf-8
# Author: wanhui0729@gmail.com

# Link：https://leetcode.com/problems/valid-parentheses/description

'''
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Note that an empty string is also considered valid.

Example 1:

Input: "()"
Output: true
Example 2:

Input: "()[]{}"
Output: true
Example 3:

Input: "(]"
Output: false
Example 4:

Input: "([)]"
Output: false
Example 5:

Input: "{[]}"
Output: true
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(n)
    '''
    def isValid(self, s):
        stack = []
        map = {
            '{': '}',
            '[': ']',
            '(': ')'
        }
        for c in s:
            if c in map:
                stack.append(map[c])
            else:
                top_element = stack.pop() if stack else '#'
                if c != top_element:
                    return False
        return not stack

if __name__ == '__main__':
    s = Solution()
    assert s.isValid('()') is True
    assert s.isValid('()[]{}') is True
    assert s.isValid('(]') is False
    assert s.isValid('([)]') is False
    assert s.isValid('{[]}') is True

'''
intuition
类似这种有序对对碰的思路刚好符合栈压入和弹出设计
通过遍历整个序列逐个匹配来进行验证
'''