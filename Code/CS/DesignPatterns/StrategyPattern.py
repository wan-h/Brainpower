# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个策略接口。
class Strategy(object):
    def doOperation(self, num1: int, num2: int):
        pass

# 创建实现接口的实体类。
class OperationAdd(Strategy):
    def doOperation(self, num1: int, num2: int):
        return num1 + num2
class OperationSubstract(Strategy):
    def doOperation(self, num1: int, num2: int):
        return num1 - num2
class OperationMultiply(Strategy):
    def doOperation(self, num1: int, num2: int):
        return num1 * num2

# 创建 Context 类
class Context(object):
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
    def executeStrategy(self, num1: int, num2: int):
        return self.strategy.doOperation(num1, num2)

# 使用 Context 来查看当它改变策略 Strategy 时的行为变化。
if __name__ == '__main__':
    context = Context(OperationAdd())
    print("10 + 5 = {}".format(context.executeStrategy(10, 5)))
    context = Context(OperationSubstract())
    print("10 - 5 = {}".format(context.executeStrategy(10, 5)))
    context = Context(OperationMultiply())
    print("10 * 5 = {}".format(context.executeStrategy(10, 5)))