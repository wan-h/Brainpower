# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/number-of-1-bits/description/

'''
Write a function that takes an unsigned integer and return the number of '1' bits it has (also known as the Hamming weight).

Example 1:

Input: 00000000000000000000000000001011
Output: 3
Explanation: The input binary string 00000000000000000000000000001011 has a total of three '1' bits.
Example 2:

Input: 00000000000000000000000010000000
Output: 1
Explanation: The input binary string 00000000000000000000000010000000 has a total of one '1' bit.
Example 3:

Input: 11111111111111111111111111111101
Output: 31
Explanation: The input binary string 11111111111111111111111111111101 has a total of thirty one '1' bits.

Note:
Note that in some languages such as Java, there is no unsigned integer type. In this case, the input will be given as signed integer type and should not affect your implementation, as the internal binary representation of the integer is the same whether it is signed or unsigned.
In Java, the compiler represents the signed integers using 2's complement notation. Therefore, in Example 3 above the input represents the signed integer -3.
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def hammingWeight(self, n):
        count = 0
        while n:
            n &= (n - 1)
            count += 1
        return count

if __name__ == '__main__':
    s = Solution()
    assert s.hammingWeight(11) == 3

'''
intuition
主要是需要熟练位运算的计算方式
n & (n - 1)可以消除n二进制的最后一个1
'''