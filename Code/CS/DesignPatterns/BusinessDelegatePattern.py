# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建 BusinessService 接口。
class BusinessService(object):
    def doProcessing(self):
        pass

# 创建实体服务类。
class EJBService(BusinessService):
    def doProcessing(self):
        print("Processing task by invoking EJB Service")
class JMSService(BusinessService):
    def doProcessing(self):
        print("Processing task by invoking JMS Service")

# 创建业务查询服务
class BusinessLookUp(object):
    def getBusinessService(self, serviceType: str):
        if serviceType == 'EJB':
            return EJBService()
        else:
            return JMSService()

# 创建业务代表。
class BusinessDelegate(object):
    lookupService = BusinessLookUp()
    businessService = None
    serviceType = ""
    def setServiceType(self, serviceType: str):
        self.serviceType = serviceType
    def doTask(self):
        self.businessService = self.lookupService.getBusinessService(self.serviceType)
        self.businessService.doProcessing()

# 创建客户端。
class Client(object):
    def __init__(self, businessService: BusinessDelegate):
        self.businessService = businessService
    def doTask(self):
        self.businessService.doTask()


# 使用 BusinessDelegate 和 Client 类来演示业务代表模式。
if __name__ == '__main__':
    businessDelegate = BusinessDelegate()
    businessDelegate.setServiceType("EJB")
    client = Client(businessDelegate)
    client.doTask()

    businessDelegate.setServiceType("JMS")
    client.doTask()