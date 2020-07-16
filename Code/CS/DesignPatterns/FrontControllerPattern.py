# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建视图。
class HomeView(object):
    def show(self):
        print("Displaying Home Page")

class StudentView(object):
    def show(self):
        print("Displaying Student Page")

# 创建调度器 Dispatcher。
class Dispatcher(object):
    def __init__(self):
        self.studentView = StudentView()
        self.homeView = HomeView()
    def dispatch(self, request: str):
        if request == 'STUDENT':
            self.studentView.show()
        else:
            self.homeView.show()

# 创建前端控制器 FrontController。
class FrontController(object):
    def __init__(self):
        self.dispatcher = Dispatcher()
    def isAuthenticUser(self):
        print("User is authenticated successfully.")
        return True
    def trackRequest(self, request: str):
        print("Page requested: {}".format(request))
    def dispatchRequest(self, request: str):
        self.trackRequest(request)
        if self.isAuthenticUser():
            self.dispatcher.dispatch(request)

# 使用 FrontController 来演示前端控制器设计模式。
if __name__ == '__main__':
    frontController = FrontController()
    frontController.dispatchRequest("HOME")
    frontController.dispatchRequest("STUDENT")