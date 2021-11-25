# coding: utf-8
# Author: wanhui0729@gmail.com

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 创建随机队列，exclusive=True表示没有消费者链接后将删除队列，result.method.queue为随机队列的名称
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# 启动多个worker,和logs exchange绑定的队列都将接受到消息
channel.start_consuming()