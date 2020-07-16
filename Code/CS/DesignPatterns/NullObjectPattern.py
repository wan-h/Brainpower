# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个抽象类。
class AbstractCustomer(object):
    name = ''
    def isNil(self):
        pass
    def getName(self):
        pass

# 创建扩展了上述类的实体类。
class RealCustomer(AbstractCustomer):
    def __init__(self, name: str):
        self.name = name

    def getName(self):
        return self.name

    def isNil(self):
        return False

class NullCustomer(AbstractCustomer):
    def getName(self):
        return "Not Available in Customer Database"
    def isNil(self):
        return True

# 创建 CustomerFactory 类。
class CustomerFactory(object):
    names = ['Rob', 'Joe', 'Julie']
    @classmethod
    def getCustomer(cls, name: str):
        for i in range(len(cls.names)):
            if cls.names[i] == name:
                return RealCustomer(name)
        return NullCustomer()

# 使用 CustomerFactory，基于客户传递的名字，来获取 RealCustomer 或 NullCustomer 对象。
if __name__ == '__main__':
    customer1 = CustomerFactory.getCustomer("Rob")
    customer2 = CustomerFactory.getCustomer("Bob")
    customer3 = CustomerFactory.getCustomer("Julie")
    customer4 = CustomerFactory.getCustomer("Laura")

    print("Customers:")
    print(customer1.getName())
    print(customer2.getName())
    print(customer3.getName())
    print(customer4.getName())