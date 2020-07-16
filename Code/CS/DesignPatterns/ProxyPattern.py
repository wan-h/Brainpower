# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个接口。
class Image(object):
    def display(self):
        pass

# 创建实现接口的实体类。
class RealImage(Image):
    def __init__(self, fileName: str):
        self.fileName = fileName
        self.loadFromDisk(fileName)
    def display(self):
        print("Displaying {}".format(self.fileName))
    def loadFromDisk(self, fileName: str):
        print("Loading {}".format(fileName))
class ProxyImage(Image):
    def __init__(self, fileName: str):
        self.fileName = fileName
        self.realImage = None
    def display(self):
        if self.realImage is None:
            self.realImage = RealImage(self.fileName)
        self.realImage.display()

# 当被请求时，使用 ProxyImage 来获取 RealImage 类的对象。
if __name__ == '__main__':
    image = ProxyImage("test_10mb.jpg")
    # 图像将从磁盘加载
    image.display()
    print("")
    # 图像不需要从磁盘加载
    image.display()
