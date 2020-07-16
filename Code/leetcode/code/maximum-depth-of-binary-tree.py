# coding: utf-8
# Author: wanhui0729@gmail.com

# Link：https://leetcode.com/problems/maximum-depth-of-binary-tree/description/

'''

Given a binary tree, find its maximum depth.

The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Note: A leaf is a node with no children.

Example:

Given binary tree [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
return its depth = 3.
'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import TreeNode

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(logn)
    '''
    def maxDepth(self, root):
        if root is None:
            return 0
        else:
            return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1

if __name__ == '__main__':
    s = Solution()
    input = TreeNode(3)
    input.left = TreeNode(9)
    input.right = TreeNode(20)
    input.right.left = TreeNode(15)
    input.right.right = TreeNode(7)
    assert s.maxDepth(input) == 3

'''
intuition
二叉树是一种递归的数据结构，刚好符合二叉树使用递归解决问题的思想。
'''