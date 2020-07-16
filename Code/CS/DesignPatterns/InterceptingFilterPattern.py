# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建过滤器接口 Filter。
class Filter(object):
    def execute(self, request: str):
        pass

# 创建实体过滤器。
class AuthenticationFilter (Filter):
    def execute(self, request: str):
        print("Authenticating  log: {}".format(request))

class DebugFilter(Filter):
    def execute(self, request: str):
        print("request log: {}".format(request))

# 创建 Target。
class Target(object):
    def execute(self, request: str):
        print("Executing request: {}".format(request))

# 创建过滤器链。
class Filterchain():
    filters = []
    target = None
    def addFilter(self, filter: Filter):
        self.filters.append(filter)

    def execute(self, request: str):
        for filter in self.filters:
            filter.execute(request)
        self.target.execute(request)

    def setTarget(self, target: Target):
        self.target = target

# 创建过滤管理器。
class FilterManager(object):
    def __init__(self, target: Target):
        self.filterChain = Filterchain()
        self.filterChain.setTarget(target)

    def setFilter(self, filter: Filter):
        self.filterChain.addFilter(filter)

    def filterRequest(self, request: str):
        self.filterChain.execute(request)

# 创建客户端 Client。
class Client(object):
    filterManager = None
    def setFilterManager(self, filterManager: FilterManager):
        self.filterManager = filterManager

    def sendRequest(self, request: str):
        self.filterManager.filterRequest(request)

# 使用 Client 来演示拦截过滤器设计模式。
if __name__ == '__main__':
    filterManager = FilterManager(Target())
    filterManager.setFilter(AuthenticationFilter())
    filterManager.setFilter(DebugFilter())

    client = Client()
    client.setFilterManager(filterManager)
    client.sendRequest("HOME")