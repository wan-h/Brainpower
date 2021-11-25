# coding: utf-8
# Author: wanhui0729@gmail.com

import redis

# master可读写, slaver只能读
r = redis.Redis(host='10.100.4.15', port=30225, db=0)
print(r.set('foo', 'bar'))
print(r.get('foo'))
print(r.delete('foo'))
