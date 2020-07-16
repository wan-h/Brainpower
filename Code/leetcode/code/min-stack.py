# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/min-stack/description/

'''
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
Example:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.
'''

class MinStack(object):
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.min = float('inf')
        self.stack = []

    def push(self, x: int):
        self.stack.append(x - self.min)
        if x < self.min:
            self.min = x

    def pop(self):
        if not self.stack:
            return
        tmp = self.stack.pop()
        if tmp < 0:
            self.min -= tmp

    def top(self):
        if not self.stack:
            return
        tmp = self.stack[-1]
        if tmp < 0:
            return self.min
        else:
            return self.min + tmp

    def getMin(self):
        return self.min

if __name__ == '__main__':
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2

'''
intuition
为了即时获得最小值则在每次操作时候重新计算最小值
栈中存储的元素为与当前最小值的差值，则在计算当前时可以通过最小值进行反推
虽然这个栈增加了普通入栈出栈的复杂度，但是将获取栈最小值的复杂度做到了O(1)
'''