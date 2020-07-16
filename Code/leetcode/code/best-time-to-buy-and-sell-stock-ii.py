# coding: utf-8
# Author: wanhui0729@gmail.com

# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/

'''
Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times).

Note: You may not engage in multiple transactions at the same time (i.e., you must sell the stock before you buy again).

Example 1:

Input: [7,1,5,3,6,4]
Output: 7
Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
             Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
Example 2:

Input: [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
             Note that you cannot buy on day 1, buy on day 2 and sell them later, as you are
             engaging multiple transactions at the same time. You must sell before buying again.
Example 3:

Input: [7,6,4,3,1]
Output: 0
Explanation: In this case, no transaction is done, i.e. max profit = 0.
'''

class Solution(object):
    '''
    时间复杂度: O(n)
    空间复杂度: O(1)
    '''
    def maxProfit(self, prices):
        if not prices: return 0
        gains = [prices[i] - prices[i - 1] for i in range(1, len(prices)) if prices[i] - prices[i - 1] > 0]
        return sum(gains)

if __name__ == '__main__':
    s = Solution()
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 7
    assert s.maxProfit([1, 2, 3, 4, 5]) == 4
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0

'''
intuition
分析问题，模拟买入卖出需要找到走势凹点和凸点，但是其结果就是所有正收益的差值，不需要模拟只需要计算正收益就可以得到理想最大结果。
所以在计算理想最值的时候可以跳出问题的描述约束寻找一些直接解法。
'''