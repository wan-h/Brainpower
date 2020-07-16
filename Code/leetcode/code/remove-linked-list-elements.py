# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/remove-linked-list-elements/description/

'''
Remove all elements from a linked list of integers that have value val.

Example:

Input:  1->2->6->3->4->5->6, val = 6
Output: 1->2->3->4->5
'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import ListNode

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def removeElements(self, head, val):
        prev = ListNode(0)
        prev.next = head
        cur = prev
        while cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return prev.next

if __name__ == '__main__':
    s = Solution()
    input_vals = [1, 2, 6, 3, 4, 5, 6]
    input_link_head = ListNode(0)
    tmp = input_link_head
    for val in input_vals:
        tmp.next = ListNode(val)
        tmp = tmp.next

    output = s.removeElements(input_link_head.next, 6)
    output_list = []
    tmp = output
    while tmp:
        output_list.append(tmp.val)
        tmp = tmp.next
    assert output_list == [1, 2, 3, 4, 5]

'''
intuition
链表删除操作，使用直接循环修改链表的指针指向即可
'''