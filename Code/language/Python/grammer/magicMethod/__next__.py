# coding: utf-8
# Author: wanhui0729@gmail.com

class MyIterator_1():
    def __init__(self, num):
        self.num = num

    def __iter__(self):
        '''
        返回迭代器对象, 该类有__next__方法，见下代码
        '''
        return self

    def __next__(self):
        self.num -= 1
        if self.num < 0:
            raise StopIteration
        else:
            return self.num

class MyIterator_3():
    def __init__(self, num):
        self.num = num
    def __next__(self):
        self.num -= 1
        if self.num < 0:
            raise StopIteration
        else:
            return self.num

class MyIterator_2():
    def __init__(self, num):
        self.num = num

    def __iter__(self):
        return MyIterator_3(self.num)


if __name__ == '__main__':
    for i in MyIterator_1(10):
        print(i)
    for i in MyIterator_2(10):
        print(i)