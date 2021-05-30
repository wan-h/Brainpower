# coding: utf-8
# Author: wanhui0729@gmail.com

'''
python使用位运算实现四则运算
'''

class Arithmometer(object):
    # 模拟32位
    MASK = 0xFFFFFFFF
    @classmethod
    def add(cls, a, b):
        '''
        在 Python 中，整数不是 32 位的，需要手动对 Python 中的整数进行处理，模拟 32 位 INT 整型
        '''
        a &= cls.MASK
        b &= cls.MASK
        while b:
            carry = (a & b) << 1
            a = (a ^ b)
            # python的左移是有问题的，会一直翻倍
            b = carry & cls.MASK
        # 0x80000000 开始为负数
        return a if a < 0x80000000 else ~(a ^ 0xFFFFFFFF)

    @classmethod
    def subtraction(cls, a, b):
        return cls.add(a, -b)

if __name__ == '__main__':
    print(Arithmometer.add(1, -1))
    print(Arithmometer.subtraction(10, 1))