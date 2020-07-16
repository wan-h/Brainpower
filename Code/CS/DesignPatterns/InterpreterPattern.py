# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个表达式接口。
class Expression(object):

    def interpret(self, context: str):
        pass

# 创建实现了上述接口的实体类。
class TerminalExpression(Expression):
    _data = ""

    def __init__(self, data: str):
        self._data = data

    def interpret(self, context: str):
        if self._data in context:
            return True
        return False

class OrExpression(Expression):
    _expr1 = None
    _expr2 = None

    def __init__(self, expr1: Expression, expr2: Expression):
        self._expr1 = expr1
        self._expr2 = expr2

    def interpret(self, context: str):
        return self._expr1.interpret(context) or self._expr2.interpret(context)

class AndExpression(Expression):
    _expr1 = None
    _expr2 = None

    def __init__(self, expr1: Expression, expr2: Expression):
        self._expr1 = expr1
        self._expr2 = expr2

    def interpret(self, context: str):
        return self._expr1.interpret(context) and self._expr2.interpret(context)

# InterpreterPatternDemo 使用 Expression 类来创建规则，并解析它们。
if __name__ == '__main__':
    # 规则：Robert和John是男性
    def getMaleExpression():
        rebert = TerminalExpression("Robert")
        john = TerminalExpression("John")
        return OrExpression(rebert, john)

    # 规则：Julie是一个已婚的女性
    def getMarriedWomanExpression():
        julie = TerminalExpression("Julie")
        married = TerminalExpression("Married")
        return AndExpression(julie, married)

    isMale = getMaleExpression()
    isMarriedWoman = getMarriedWomanExpression()
    print("John is male? {}".format(isMale.interpret("John")))
    print("Julie is a married women? {}".format(isMarriedWoman.interpret("Married Julie")))