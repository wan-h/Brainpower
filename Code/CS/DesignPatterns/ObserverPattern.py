# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建 Subject 类。
class Subject(object):
    observers = []
    state = 0

    def getState(self):
        return self.state

    def setState(self, state: int):
        self.state = state
        self.notifyAllObservers()

    def attach(self, observer):
        self.observers.append(observer)

    def notifyAllObservers(self):
        for observer in self.observers:
            observer.update()

# 创建 Observer 类
class Observer(object):
    subject = None

    def update(self):
        pass

# 创建实体观察者类。
class BinaryObserver(Observer):
    def __init__(self, subject: Subject):
        self.subject = subject
        self.subject.attach(self)

    def update(self):
        print("Binary String: {}".format(bin(self.subject.getState())))

class OctalObserver(Observer):
    def __init__(self, subject: Subject):
        self.subject = subject
        self.subject.attach(self)

    def update(self):
        print("Octal String: {}".format(oct(self.subject.getState())))

class HexaObserver(Observer):
    def __init__(self, subject: Subject):
        self.subject = subject
        self.subject.attach(self)

    def update(self):
        print("Hex String: {}".format(hex(self.subject.getState())))

# 使用 Subject 和实体观察者对象。
if __name__ == '__main__':
    subject = Subject()
    HexaObserver(subject)
    OctalObserver(subject)
    BinaryObserver(subject)

    print("First state change: 15")
    subject.setState(15)
    print("Second state change: 10")
    subject.setState(10)