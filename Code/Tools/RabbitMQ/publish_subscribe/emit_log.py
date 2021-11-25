# coding: utf-8
# Author: wanhui0729@gmail.com

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 生产的消息是通过exchange再转发到队列的
# fanout模式表示exchange将消息广播到他知道的所有队列中
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
# 如果没有exchange绑定的队列，消息将会丢失，因为没有消费者
channel.basic_publish(exchange='logs', routing_key='', body=message)

print(" [x] Sent %r" % message)
connection.close()