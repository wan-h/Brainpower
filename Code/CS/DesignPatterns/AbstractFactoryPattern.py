# coding: utf-8
# Author: wanhui0729@gmail.com

# 为形状创建一个接口
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

# 为颜色创建一个接口。
class Color(object):
    def fill(self):
        pass
# 实现color的实体类
class Red(Color):
    def fill(self):
        print("Inside Red::fill() method.")
class Green(Color):
    def fill(self):
        print("Inside Green::fill() method.")
class Blue(Color):
    def fill(self):
        print("Inside Blue::fill() method.")

# 为 Color 和 Shape 对象创建抽象类来获取工厂。
class AbstractFactiry(object):
    def getColor(self, shapeType: str):
        pass
    def getShape(self, colorType: str):
        pass

# 创建扩展了 AbstractFactory 的工厂类，基于给定的信息生成实体类的对象。
class ShapeFactory(AbstractFactiry):
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
    def getColor(self, colorType: str):
        return None
class ColorFactory(AbstractFactiry):
    def getShape(self, shapeType: str):
        return None
    def getColor(self, colorType: str):
        if colorType is None:
            return None
        if colorType == 'RED':
            return Red()
        elif colorType == 'GREEN':
            return Green()
        elif colorType == 'BLUE':
            return Blue()
        return None

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

# 创建一个工厂创造器/生成器类，通过传递形状或颜色信息来获取工厂。
class FactoryProducer(object):
    @classmethod
    def getFactory(self, choice: str):
        if choice == 'SHAPE':
            return ShapeFactory()
        elif choice == 'COLOR':
            return ColorFactory()
        return None

# 使用 FactoryProducer 来获取 AbstractFactory，通过传递类型信息来获取实体类的对象。
if __name__ == '__main__':
    shapeFactory = FactoryProducer.getFactory('SHAPE')
    shape1 = shapeFactory.getShape('CIRCLE')
    shape1.draw()
    shape2 = shapeFactory.getShape('RECTANGLE')
    shape2.draw()
    shape3 = shapeFactory.getShape('SQUARE')
    shape3.draw()
    colorFactory = FactoryProducer.getFactory('COLOR')
    color1 = colorFactory.getColor('RED')
    color1.fill()
    color2 = colorFactory.getColor('GREEN')
    color2.fill()
    color3 = colorFactory.getColor('BLUE')
    color3.fill()