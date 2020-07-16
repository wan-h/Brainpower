# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个命令接口。
class Order(object):
    def execute(self):
        pass

# 创建一个请求类。
class Stock(object):
    def __init__(self):
        self.name = 'ABC'
        self.quantity = 10
    def buy(self):
        print("Stock [Name: {}, Quantity: {}] bought".format(self.name, self.quantity))
    def sell(self):
        print("Stock [Name: {}, Quantity: {}] sold".format(self.name, self.quantity))

# 创建实现了 Order 接口的实体类。
class BuyStock(Order):
    def __init__(self, abcStock: Stock):
        self.abcStock = abcStock
    def execute(self):
        self.abcStock.buy()
class SellStock(Order):
    def __init__(self, abcStock: Stock):
        self.abcStock = abcStock
    def execute(self):
        self.abcStock.sell()

# 创建命令调用类。
class Broker(object):
     def __init__(self):
         self.orderList = []
     def takeOrder(self, order: Order):
         self.orderList.append(order)
     def placeOrders(self):
         for order in self.orderList:
             order.execute()
         self.orderList.clear()


# 使用 Broker 类来接受并执行命令。
if __name__ == '__main__':
    abcStock = Stock()
    buyStockOrder = BuyStock(abcStock)
    sellStockOrder = SellStock(abcStock)

    broker = Broker()
    broker.takeOrder(buyStockOrder)
    broker.takeOrder(sellStockOrder)

    broker.placeOrders()