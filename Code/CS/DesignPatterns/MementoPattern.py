# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建Memento类
class Memento(object):
    _state = ""
    def __init__(self, strState):
        self._state = strState
    def getState(self):
        return self._state

# 创建Originator类
class Originator(object):
    _state = ""
    def setState(self, strState):
        self._state = strState
    def getState(self):
        return self._state
    def saveStateToMemento(self):
        return Memento(self._state)
    def getStateFromMemento(self, inMemento):
        self._state = inMemento.getState()

# 创建CareTaker类
class CareTaker(object):
    _mementoList = []
    def add(self, inMemento):
        self._mementoList.append(inMemento)
    def get(self, inIndex):
        return self._mementoList[inIndex]

# 调用输出
if __name__ == '__main__':
    originator = Originator()
    careTaker = CareTaker()

    originator.setState("State #1")
    originator.setState("State #2")
    careTaker.add(originator.saveStateToMemento())
    originator.setState("State #3")
    careTaker.add(originator.saveStateToMemento())
    originator.setState("State #4")

    print("Current State: {}".format(originator.getState()))
    originator.getStateFromMemento(careTaker.get(0))
    print("First saved State: {}".format(originator.getState()))
    originator.getStateFromMemento(careTaker.get(1))
    print("First saved State: {}".format(originator.getState()))