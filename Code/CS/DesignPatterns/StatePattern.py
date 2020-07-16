# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个接口。
class State(object):
    def doAction(self):
        pass

# 创建实现接口的实体类。
class StartState(State):
    def doAction(self, context):
        print("Player is in start state")
        context.setState(self)
    def toString(self):
        return "Start State"

class StopState(State):
    def doAction(self, context):
        print("Player is in stop state")
        context.setState(self)
    def toString(self):
        return "Stop State"

# 创建 Context 类。
class Context(object):
    def __init__(self):
        self.state = None

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

# 使用 Context 来查看当状态 State 改变时的行为变化。
if __name__ == '__main__':
    context = Context()
    startState = StartState()
    startState.doAction(context)
    print(context.getState().toString())

    stopState = StopState()
    stopState.doAction(context)
    print(context.getState().toString())