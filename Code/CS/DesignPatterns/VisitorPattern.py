# coding: utf-8
# Author: wanhui0729@gmail.com

# 定义一个表示元素的接口。
class ComputerPart(object):
    def accept(self, computerPartVisitor):
        pass

# 创建扩展了上述类的实体类。
class Keyboard(ComputerPart):
    def accept(self, computerPartVisitor):
        computerPartVisitor.visitKeyboard(self)

class Monitor(ComputerPart):
    def accept(self, computerPartVisitor):
        computerPartVisitor.visitMonitor(self)

class Mouse(ComputerPart):
    def accept(self, computerPartVisitor):
        computerPartVisitor.visitMouse(self)

class Computer(ComputerPart):
    parts = []
    def __init__(self):
        self.parts = [
            Mouse(),
            Keyboard(),
            Monitor()
        ]
    def accept(self, computerPartVisitor):
        for part in self.parts:
            part.accept(computerPartVisitor)
        computerPartVisitor.visitComputer(self)

# 定义一个表示访问者的接口。
class ComputerPartVisitor(object):
    def visitComputer(self, computer: Computer):
        pass
    def visitMouse(self, mouse: Mouse):
        pass
    def visitKeyboard(self, keyBoard: Keyboard):
        pass
    def visitMonitor(self, monitor: Monitor):
        pass

# 创建实现了上述类的实体访问者。
class ComputerPartDisplayVisitor(ComputerPartVisitor):
    def visitComputer(self, computer: Computer):
        print("Displaying {0}. Called in {1}".format(computer.__class__.__name__, self.__class__.__name__))
    def visitMouse(self, mouse: Mouse):
        print("Displaying {0}. Called in {1}".format(mouse.__class__.__name__, self.__class__.__name__))
    def visitKeyboard(self, keyBoard: Keyboard):
        print("Displaying {0}. Called in {1}".format(keyBoard.__class__.__name__, self.__class__.__name__))
    def visitMonitor(self, monitor: Monitor):
        print("Displaying {0}. Called in {1}".format(monitor.__class__.__name__, self.__class__.__name__))

# 使用 ComputerPartDisplayVisitor 来显示 Computer 的组成部分。
if __name__ == '__main__':
    computer = Computer()
    computer.accept(ComputerPartDisplayVisitor())