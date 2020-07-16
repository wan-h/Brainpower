# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建依赖对象。
class DependentObject1(object):
    data = ""
    def setData(self, data: str):
        self.data = data

    def getData(self):
        return self.data

class DependentObject2(object):
    data = ""
    def setData(self, data: str):
        self.data = data

    def getData(self):
        return self.data

# 创建粗粒度对象。
class CoarseGrainedObject(object):
    do1 = DependentObject1()
    do2 = DependentObject2()
    def setdata(self, data1: str, data2: str):
        self.do1.setData(data1)
        self.do2.setData(data2)

    def getData(self):
        return [self.do1.getData(), self.do2.getData()]

# 创建组合实体。
class CompositeEntity(object):
    cgo = CoarseGrainedObject()
    def setData(self, data1: str, data2: str):
        self.cgo.setdata(data1, data2)

    def getdata(self):
        return self.cgo.getData()

# 创建使用组合实体的客户端类。
class Client(object):
    compositeEntity = CompositeEntity()
    def printData(self):
        for data in self.compositeEntity.getdata():
            print("Data: {}".format(data))

    def setdata(self, data1: str, data2: str):
        self.compositeEntity.setData(data1, data2)


# 使用 Client 来演示组合实体设计模式的用法。
if __name__ == '__main__':
    client = Client()
    client.setdata("Test", "Data")
    client.printData()
    client.setdata("Second Test", "Data1")
    client.printData()