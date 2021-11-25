# coding: utf-8
# Author: wanhui0729@gmail.com

'''
可以同时启动两个worker一起消费，默认情况下平均分配任务
'''

import os, sys
import time
import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 创建中间件队列,多次执行也只会创建一个
    # durable标志进行持久化存储，防止队列服务死掉后数据丢失
    # 一个已经创建的非持久化队列不可在被申明创建为一个持久化队列
    channel.queue_declare(queue='task_queue', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")

    # 平均分配策略并不是一直好用，消息处理的耗时不同可能导致某些worker消息分配积压
    # prefetch_count=1表示确认处理完之后再发送给worker消息，优先发送给其他空闲的worker
    channel.basic_qos(prefetch_count=1)
    # auto_ack=False表示woker执行完成后需要向队列返回结束信息,确保内容不会丢失
    # 如果队列的worker连接丢失切没有收到回复信息，则队列重新将消息发送给其他的worker
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
