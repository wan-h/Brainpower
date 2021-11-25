# coding: utf-8
# Author: wanhui0729@gmail.com

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建中间件队列
channel.queue_declare(queue='hello')

# 发布消息，routing_key指定队列名字，消息不直接入队列，通过exchange环节
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body=message,
    # 生产者持久化存储设置
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)
print(" [x] Sent %r" % message)
# 确保网络缓冲区已刷新并且消息实际上已传递到RabbitMQ
connection.close()