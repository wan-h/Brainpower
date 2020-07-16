# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建桥接实现接口。
class DrawAPI(object):
    def drawCircle(self, radius: int, x: int, y: int):
        pass

# 创建实现了 DrawAPI 接口的实体桥接实现类。
class RedCircle(DrawAPI):
    def drawCircle(self, radius: int, x: int, y: int):
        print("Drawing Circle[ color: red, radius: {}, x: {}, y: {}]".format(radius, x, y))
class GreenCircle(DrawAPI):
    def drawCircle(self, radius: int, x: int, y: int):
        print("Drawing Circle[ color: green, radius: {}, x: {}, y: {}]".format(radius, x, y))

# 使用 DrawAPI 接口创建抽象类 Shape。
class Shape(object):
    def __init__(self, drawAPI: DrawAPI):
        self.drawAPI = drawAPI
    def draw(self):
        pass

# 创建实现了 Shape 接口的实体类。
class Circle(Shape):
    def __init__(self, x: int, y: int, radius: int, drawAPI: DrawAPI):
        super(Circle, self).__init__(drawAPI)
        self.x = x
        self.y = y
        self.radius = radius
    def draw(self):
        self.drawAPI.drawCircle(self.radius, self.x, self.y)


if __name__ == '__main__':
    redCircle = Circle(100, 100, 10, RedCircle())
    greenCircle = Circle(100, 100, 10, GreenCircle())
    redCircle.draw()
    greenCircle.draw()