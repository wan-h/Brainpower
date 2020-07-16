# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/reverse-linked-list/description/

'''
Reverse a singly linked list.

Example:

Input: 1->2->3->4->5->NULL Output: 5->4->3->2->1->NULL Follow up:

A linked list can be reversed either iteratively or recursively. Could you implement both?
'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import ListNode

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def reverseList(self, head):
        if not head: return None
        prev = None
        cur = head
        while cur:
            tmp = cur.next
            cur.next = prev
            prev = cur
            cur = tmp
        return prev

if __name__ == '__main__':
    s = Solution()
    input_vals = [1, 2, 3, 4, 5]
    input_link_head = ListNode(0)
    tmp = input_link_head
    for val in input_vals:
        tmp.next = ListNode(val)
        tmp = tmp.next

    output = s.reverseList(input_link_head.next)
    output_list = []
    tmp = output
    while tmp:
        output_list.append(tmp.val)
        tmp = tmp.next

    assert output_list == [5, 4, 3, 2, 1]

'''
intuition
链表翻转操作，遍历链表修改链表的指针即可
'''