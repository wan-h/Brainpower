# coding: utf-8
# Author: wanhui0729@gmail.com

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 生产的消息是通过exchange再转发到队列的
# direct模式在exchange和队列之间建立一个路由算法，将消息路由到binding key和routing key匹配的队列
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
# routing_key指定路由关键字
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()