# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个接口。
class Shape(object):
    def draw(self):
        pass

# 创建实现接口的实体类。
class Circle(Shape):
    def __init__(self, color: str):
        self.color = color
        self.x = None
        self.y = None
        self.radius = None
    def setX(self, x: int):
        self.x = x
    def setY(self, y: int):
        self.y = y
    def setRadius(self, radius: int):
        self.radius = radius
    def draw(self):
        print("Circle: Draw() [Color: {}, x: {}, y: {}, radius: {}]".
              format(self.color, self.x, self.y, self.radius))

# 创建一个工厂，生成基于给定信息的实体类的对象。
class ShapeFactory(object):
    circleMap = {}
    @classmethod
    def getCircle(cls, color: str):
        circle = cls.circleMap.get(color)
        if circle is None:
            circle = Circle(color)
            cls.circleMap[color] = circle
            print("Creating circle of color: {}".format(color))
        return circle

# 使用该工厂，通过传递颜色信息来获取实体类的对象。
import random
if __name__ == '__main__':
    colors = ['Red', 'Green', 'Blue', 'White', 'Black']
    for i in range(20):
        color = random.choice(colors)
        circle = ShapeFactory.getCircle(color)
        circle.setX(random.randint(1, 100))
        circle.setY(random.randint(1, 100))
        circle.setRadius(100)
        circle.draw()