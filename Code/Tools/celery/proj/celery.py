# coding: utf-8
# Author: wanhui0729@gmail.com

'''
启动broker作为测试
rabbitMQ: docker run --rm -d -p 5672:5672 -p 15672:15672 rabbitmq
redis: docker run --rm -d -p 6379:6379 redis
安装python包
pip install rabbitmq
pip install redis

rabbit进入容器设置用户
$ rabbitmqctl add_user myuser mypassword
$ rabbitmqctl add_vhost myvhost
$ rabbitmqctl set_user_tags myuser mytag
$ rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
'''

# 拒绝隐式引入，因为celery.py的名字和celery的包名冲突
from __future__ import absolute_import
from celery import Celery

# 实例化celery对象
app = Celery(
    'proj',
    include=['proj.task']
)

# 配置文件加载
app.config_from_object('proj.celeryconfig')

# 使用以下命令启动worker
# celery -A proj worker -l info

# 使用flower可视化监管任务启动(https://flower-docs-cn.readthedocs.io/zh/latest)
# flower --address=127.0.0.1 --port=5555 -A proj
# flower访问地址: http://127.0.0.1:5555/

if __name__ == '__main__':
    app.start()