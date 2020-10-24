# coding: utf-8
# Author: wanhui0729@gmail.com

import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    # 用户在每个任务执行后等待5到9秒
    wait_time = between(5, 9)

    @task
    def index_page(self):
        self.client.get("/hello")
        self.client.get("/world")

    # 分配任务被选择的权重
    @task(3)
    def view_item(self):
        item_id = random.randint(1, 10000)
        # 我们使用名称参数将所有这些请求分组到一个名为的条目下"/item"，避免统计信息时全是独立单独的条目
        self.client.get(f"/item?id={item_id}", name="/item")

    # 每个模拟用户在启动时都会调用具有该名称的方法
    def on_start(self):
        self.client.post("/login", {"username": "foo", "password": "bar"})

'''
使用bash启动locust开始测试
eg: locust -f locust_files/my_locust_file.py --host http://0.0.0.0:5000 --web-host 0.0.0.0
先关参数见https://docs.locust.io/en/stable/configuration.html
'''