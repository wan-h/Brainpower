# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/add-two-numbers/description/

'''
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order
and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example:
Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807.
'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import ListNode

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(n)
    '''
    def addTwoNumbers(self, list1, list2):
        result = ListNode(0)
        result_tail = result
        carry = 0
        while list1 or list2 or carry:
            val1 = list1.val if list1 else 0
            val2 = list2.val if list2 else 0
            carry, out = divmod(val1 + val2 + carry, 10)
            result_tail.next = ListNode(out)
            result_tail = result_tail.next

            list1 = list1.next if list1 else None
            list2 = list2.next if list2 else None
        return result.next

if __name__ == '__main__':
    s = Solution()
    list1 = ListNode(2)
    list1.next = ListNode(4)
    list1.next.next = ListNode(3)
    list2 = ListNode(5)
    list2.next = ListNode(6)
    list2.next.next = ListNode(4)
    result = s.addTwoNumbers(list1, list2)
    assert result.val == 7
    assert result.next.val == 0
    assert result.next.next.val == 8

'''
intuition
使用python的内建函数divmod简化代码
通过分析题目并对链表进行操作来解决问题
'''