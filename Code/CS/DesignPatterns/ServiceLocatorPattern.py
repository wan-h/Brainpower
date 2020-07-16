# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建服务接口 Service。
class Service(object):
    def getName(self):
        pass
    def execute(self):
        pass

# 创建实体服务。
class Service1(Service):
    def execute(self):
        print("Executing Service1")
    def getName(self):
        return "Service1"

class Service2(Service):
    def execute(self):
        print("Executing Service2")
    def getName(self):
        return "Service2"

# 为 JNDI 查询创建 InitialContext。
class InitialContext(object):
    def lookup(self, jndiName: str):
        if jndiName == 'Service1':
            print("Looking up and creating a new Service1 object")
            return Service1()
        elif jndiName == 'Service2':
            print("Looking up and creating a new Service2 object")
            return Service2()
        return None

# 创建缓存 Cache。
class Cache(object):
    def __init__(self):
        self.services = []

    def getService(self, serviceName: str):
        for service in self.services:
            if service.getName() == serviceName:
                print("Returning cache {} object".format(serviceName))
                return service
        return None

    def addService(self, newService: Service):
        exists = False
        for service in self.services:
            if service.getName() == newService.getName():
                exists = True
        if not exists:
            self.services.append(newService)

# 创建服务定位器。
class ServiceLocator(object):
    cache = Cache()
    @classmethod
    def getService(cls, jndiName: str):
        service = cls.cache.getService(jndiName)
        if service is not None:
            return service

        context = InitialContext()
        service = context.lookup(jndiName)
        cls.cache.addService(service)
        return service

# 使用 ServiceLocator 来演示服务定位器设计模式。
if __name__ == '__main__':
    service = ServiceLocator.getService("Service1")
    service.execute()
    service = ServiceLocator.getService("Service2")
    service.execute()
    service = ServiceLocator.getService("Service1")
    service.execute()
    service = ServiceLocator.getService("Service2")
    service.execute()

