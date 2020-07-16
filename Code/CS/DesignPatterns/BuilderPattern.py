# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个表示食物条目和食物包装的接口。
class Item(object):
    def name(self):
        pass
    def packing(self):
        pass
    def price(self):
        pass

class Packing(object):
    def pack(self):
        pass

# 创建实现 Packing 接口的实体类。
class Wrapper(Packing):
    def pack(self):
        return "Wrapper"

class Bottle(Packing):
    def pack(self):
        return "Bottle"

# 创建实现 Item 接口的抽象类，该类提供了默认的功能。
class Burger(Item):
    def packing(self):
        return Wrapper()
    def price(self):
        pass
class ColdDrink(Item):
    def packing(self):
        return Bottle()
    def price(self):
        pass

# 创建扩展了 Burger 和 ColdDrink 的实体类。
class VegBurger(Burger):
    def price(self):
        return 25.0
    def name(self):
        return "Veg Burger"
class ChickenBurger(Burger):
    def price(self):
        return 50.5
    def name(self):
        return "Chicken Burger"
class Coke(ColdDrink):
    def price(self):
        return 30.0
    def name(self):
        return "Coke"
class Pepsi(ColdDrink):
    def price(self):
        return 35.0
    def name(self):
        return "Pepsi"

# 创建一个 Meal 类，带有上面定义的 Item 对象。
class Meal(object):
    def __init__(self):
        self.items = list()
    def addItem(self, item):
        self.items.append(item)
    def getCost(self):
        cost = 0.0
        for item in self.items:
            cost += item.price()
        return cost
    def showItems(self):
        for item in self.items:
            print("Item : {}, Packing : {}, Price : {}".format(item.name(), item.packing().pack(), item.price()))


# 创建一个 MealBuilder 类，实际的 builder 类负责创建 Meal 对象。
class MealBuilder():
    def prepareVegMeal(self):
        meal = Meal()
        meal.addItem(VegBurger())
        meal.addItem(Coke())
        return meal
    def prepareNonVegMeal(self):
        meal = Meal()
        meal.addItem(ChickenBurger())
        meal.addItem(Pepsi())
        return meal

if __name__ == '__main__':
    mealBuilder = MealBuilder()
    vegMeal = mealBuilder.prepareVegMeal()
    print("Veg Meal")
    vegMeal.showItems()
    print("Total Cost: {}".format(vegMeal.getCost()))

    nonVegMeal = mealBuilder.prepareNonVegMeal()
    print("\n\nNon-Veg Meal")
    nonVegMeal.showItems()
    print("Total Cost: {}".format(nonVegMeal.getCost()))
