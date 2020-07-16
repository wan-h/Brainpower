# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个接口
class Shape(object):
    def draw(self):
        pass

# 创建实现接口的实体类。
class Rectangle(Shape):
    def draw(self):
        print("Shape: Rectangle")
class Circle(Shape):
    def draw(self):
        print("Shape: Circle")

# 创建实现了 Shape 接口的抽象装饰类。
class ShapeDecorator(Shape):
    def __init__(self, decoratedShape: Shape):
        self.decoratedShape = decoratedShape
    def draw(self):
        self.decoratedShape.draw()

# 创建扩展了 ShapeDecorator 类的实体装饰类。
class RedShapeDecorator(ShapeDecorator):
    def __init__(self, decoratedShape: Shape):
        super(RedShapeDecorator, self).__init__(decoratedShape)
    def setRedBorder(self, decoratedShape: Shape):
        print("Bordor Color: Red")
    def draw(self):
        self.decoratedShape.draw()
        self.setRedBorder(self.decoratedShape)

# 使用 RedShapeDecorator 来装饰 Shape 对象。
if __name__ == '__main__':
    circle = Circle()
    redCircle = RedShapeDecorator(Circle())
    redRectangle = RedShapeDecorator(Rectangle())
    print("Circle with normal border")
    circle.draw()
    print("Circle of red border")
    redCircle.draw()
    print("Rectangle of red border")
    redRectangle.draw()