# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个接口。
class Shape(object):
    def draw(self):
        pass

# 创建实现接口的实体类。
class Retangle(Shape):
    def draw(self):
        print("Rectangle::draw()")
class Square(Shape):
    def draw(self):
        print("Square::draw()")
class Circle(Shape):
    def draw(self):
        print("Circle::draw()")

# 创建一个外观类。
class ShapeMaker(object):
    def __init__(self):
        self.circle = Circle()
        self.rectangle = Retangle()
        self.square = Square()
    def drawCircle(self):
        self.circle.draw()
    def drawRectangle(self):
        self.rectangle.draw()
    def drawSquare(self):
        self.square.draw()

if __name__ == '__main__':
    shapeMaker = ShapeMaker()
    shapeMaker.drawCircle()
    shapeMaker.drawRectangle()
    shapeMaker.drawSquare()