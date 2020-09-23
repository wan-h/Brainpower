# coding: utf-8
# Author: wanhui0729@gmail.com

'''
二叉树遍历方法
'''

class Tree(object):
    '''
    Tree类
    '''
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None

def pro_order(tree):
    '''
    前序遍历
    先访问根结点，然后前序遍历左子树，再前序遍历右子树
    '''
    if tree is None:
        return None
    res.append(tree.data)
    pro_order(tree.left)
    pro_order(tree.right)

def mid_order(tree):
    '''
    中序遍历
    从根结点开始，中序遍历结点的左子树，然后访问根结点，最后中序遍历右子树
    '''
    if tree is None:
        return None
    mid_order(tree.left)
    res.append(tree.data)
    mid_order(tree.right)

def pos_order(tree):
    '''
    后序遍历
    从左到右先叶子后结点的方式遍历左右子树，最后访问根节点
    '''
    if tree is None:
        return None
    pos_order(tree.left)
    pos_order(tree.right)
    res.append(tree.data)

from collections import deque
def row_order(tree):
    '''
    层序遍历
    从树的第一层也就是根节点开始访问，从上而下逐层遍历，再同一层中从做到右的顺序对结点逐个访问
    '''
    queue = deque([tree])
    while len(queue) > 0:
        node = queue.popleft()
        res.append(node.data)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


res = []
if __name__ == '__main__':
    t = Tree(1)
    t.left = Tree(2)
    t.right = Tree(3)
    t.left.left = Tree(4)
    t.right.left = Tree(5)
    t.right.right = Tree(6)
    t.left.left.left = Tree(7)
    t.left.left.right = Tree(8)
    t.right.left.right = Tree(9)

    res.clear()
    pro_order(t)
    assert res == [1, 2, 4, 7, 8, 3, 5, 9, 6]

    res.clear()
    mid_order(t)
    assert res == [7, 4, 8, 2, 1, 5, 9, 3, 6]

    res.clear()
    pos_order(t)
    assert res == [7, 8, 4, 2, 9, 5, 6, 3, 1]

    res.clear()
    row_order(t)
    assert res == [1, 2, 3, 4, 5, 6, 7, 8, 9]