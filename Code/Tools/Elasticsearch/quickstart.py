# coding: utf-8
# Author: wanhui0729@gmail.com

'''
https://elasticsearch-py.readthedocs.io/en/master/
'''

from datetime import datetime
from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

res = es.index(index='test-index', id=1, body=doc)
print(res)

res = es.get(index='test-index', id=1)
print(res)

# ES创建内部流： doc -> index buffer -> filesystem cache -> Disk
#                        |          |          |        |
#                  不可被搜索到 -> refresh -> 可被搜索-> flush
# 使用refresh使得创建的文档可以马上被搜索到
res = es.indices.refresh(index='test-index')
print(res)

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
