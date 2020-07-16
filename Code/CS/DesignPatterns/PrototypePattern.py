# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个实现了 Cloneable 接口的抽象类
class Shape():
    def __init__(self):
        self.id = None
        self.type = None
    def draw(self):
        pass
    def getType(self):
        return self.type
    def getId(self):
        return self.id
    def setId(self, id: str):
        self.id = id

# 创建扩展了上面抽象类的实体类。
class Rectangle(Shape):
    def __init__(self):
        super(Rectangle, self).__init__()
        self.type = 'Rectangle'
    def draw(self):
        print("Inside Rectangle::draw() method.")
class Square(Shape):
    def __init__(self):
        super(Shape, self).__init__()
        self.type = 'Square'
    def draw(self):
        print("Inside Square::draw() method.")
class Circle(Shape):
    def __init__(self):
        super(Circle, self).__init__()
        self.type = 'Circle'
    def draw(self):
        print("Inside Circle::draw() method.")

# 创建一个类，从数据库获取实体类，并把它们存储在一个 Hashtable 中。
class ShapeCache(object):
    shapeMap = {}
    @classmethod
    def getShape(cls, shapeId: str):
        cachedShape = cls.shapeMap.get(shapeId)
        return cachedShape.__class__()
    @classmethod
    def loadCache(cls):
        circle = Circle()
        circle.setId('1')
        cls.shapeMap[circle.getId()] = circle
        square = Square()
        square.setId('2')
        cls.shapeMap[square.getId()] = square
        rectangle = Rectangle()
        rectangle.setId('3')
        cls.shapeMap[rectangle.getId()] = rectangle


if __name__ == '__main__':
    ShapeCache.loadCache()
    clonedShape1 = ShapeCache.getShape('1')
    print("shape : {}".format(clonedShape1.getType()))
    clonedShape1.draw()
    clonedShape2 = ShapeCache.getShape('2')
    print("shape : {}".format(clonedShape2.getType()))
    clonedShape2.draw()
    clonedShape3 = ShapeCache.getShape('3')
    print("shape : {}".format(clonedShape3.getType()))
    clonedShape3.draw()