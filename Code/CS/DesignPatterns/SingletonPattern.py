# coding: utf-8
# Author: wanhui0729@gmail.com

# 创建一个 Singleton 类。
class SingleObject(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingleObject, cls).__new__(cls, *args, **kwargs)
        return cls._instance

# 创建一个单例装饰器
from functools import wraps
def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance
@singleton
class MySingleObjectClass(object):
    pass


# 从 singleton 类获取唯一的对象。
if __name__ == '__main__':
    # 通过__new__来获取同一个实例
    object1 = SingleObject()
    object2 = SingleObject()
    print(id(object1))
    print(id(object2))
    # 通过装饰器字典来维护同一个实例
    object3 = MySingleObjectClass()
    object4 = MySingleObjectClass()
    print(id(object3))
    print(id(object4))