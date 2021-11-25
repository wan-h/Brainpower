# coding: utf-8
# Author: wanhui0729@gmail.com

import redis

class RedisQueue(object):
    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        return self.__db.llen(self.key)

    def put(self, item):
        self.__db.rpush(self.key, item)

    # 阻塞
    def get_wait(self, timeout=None):
        item = self.__db.blpop(self.key, timeout=timeout)
        return item

    # 非阻塞, 返回none
    def get_nowait(self):
        item = self.__db.lpop(self.key)
        return item

if __name__ == '__main__':
    q = RedisQueue(name='test', host='10.100.4.15', port=30225, db=0)
    for i in range(5):
        q.put(i)
        print("Redis queue set {}".format(i))

    while True:
        res = q.get_wait()
        print("Redis queue get {}".format(res))