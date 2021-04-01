# coding: utf-8
# Author: wanhui0729@gmail.com

# 可设置的配置参数 https://docs.celeryproject.org/en/stable/userguide/configuration.html

broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
result_backend = 'redis://localhost:6379/0'
# 默认队列名字
task_default_queue = 'proj'
# 开启任务状态跟踪
task_track_started = True