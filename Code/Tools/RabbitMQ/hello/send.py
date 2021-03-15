# coding: utf-8
# Author: wanhui0729@gmail.com

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建中间件队列
channel.queue_declare(queue='hello')

# 发布消息，routing_key指定队列名字，消息不直接入队列，通过exchange转发，这里为空，直接转发到名字为routing_key指定的队列
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
# 确保网络缓冲区已刷新并且消息实际上已传递到RabbitMQ
connection.close()