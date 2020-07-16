# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/invert-binary-tree/description/

'''
Invert a binary tree.

Example:

Input:

     4
   /   \
  2     7
 / \   / \
1   3 6   9
Output:

     4
   /   \
  7     2
 / \   / \
9   6 3   1
Trivia:
This problem was inspired by this original tweet by Max Howell:

Google: 90% of our engineers use the software you wrote (Homebrew), but you can’t invert a binary tree on a whiteboard so f*** off.
'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import TreeNode

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def invertTree(self, root):
        if not root:
            return None
        stack = [root]
        while stack:
            node = stack.pop(0)
            node.left, node.right = node.right, node.left
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return root


if __name__ == '__main__':
    s = Solution()
    input = TreeNode(4)
    input.left = TreeNode(2)
    input.right = TreeNode(7)
    input.left.left = TreeNode(1)
    input.left.right = TreeNode(3)
    input.right.left = TreeNode(6)
    input.right.right = TreeNode(9)
    output = s.invertTree(input)
    assert output.left.left.val == 9
    assert output.right.right.val == 1

'''
intuition
遍历树结构交换左右子树即可,通过栈的方式排队处理
'''