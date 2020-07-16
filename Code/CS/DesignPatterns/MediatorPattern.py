# coding: utf-8
# Author: wanhui0729@gmail.com

import datetime

# 创建中介类。
class ChatRoom(object):
    @classmethod
    def showMessage(cls, user, message):
        print("{} [{}] : {}".format(datetime.datetime.today(), user.getName(), message))

# 创建 user 类。
class User(object):
    def __init__(self, name: str):
        self.name = name
    def getName(self):
        return self.name
    def setName(self, name: str):
        self.name = name
    def sendMessage(self, message: str):
        ChatRoom.showMessage(self, message)

# 使用 User 对象来显示他们之间的通信。
if __name__ == '__main__':
    robert = User("Robert")
    john = User("John")
    robert.sendMessage("Hi! Jhon!")
    john.sendMessage("Hello! Robert!")