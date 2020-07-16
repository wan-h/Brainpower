# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建shape接口
class Shape(object):
    def draw(self):
        pass

# 实现shape的实体类
class Rectangle(Shape):
    def draw(self):
        print("Inside Rectangle::draw() method.")
class Square(Shape):
    def draw(self):
        print("Inside Square::draw() method.")
class Circle(Shape):
    def draw(self):
        print("Inside Circle::draw() method.")

# 创建一个工厂，生成基于给定信息的实体类的对象。
class ShapeFactory(object):
    def getShape(self, shapeType: str):
        if shapeType is None:
            return None
        if shapeType == 'CIRCLE':
            return Circle()
        elif shapeType == 'RECTANGLE':
            return Rectangle()
        elif shapeType == 'SQUARE':
            return Square()
        return None

# 使用该工厂，通过传递类型信息来获取实体类的对象。
if __name__ == '__main__':
    shapeFactory = ShapeFactory()
    shape1 = shapeFactory.getShape('CIRCLE')
    shape1.draw()
    shape2 = shapeFactory.getShape('RECTANGLE')
    shape2.draw()
    shape3 = shapeFactory.getShape('SQUARE')
    shape3.draw()