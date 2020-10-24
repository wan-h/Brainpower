# coding: utf-8
# Author: wanhui0729@gmail.com

import json
from locust import task, HttpUser, between

class MyTestUser(HttpUser):
    # wait_time: locust 定义请求间隔
    wait_time = between(0.1, 0.2)  # 模拟用户在执行每个任务之间等待的最小时间，单位为秒；

    @task
    def test_user_v0_register(self):
        data = {
            'name': 'test',
            'phone': '123456'
        }
        resp = self.client.post('/user/v0/register', json=data)
        # 确保正常返回
        resp = resp.json()
        assert resp['code'] == 0
    @task
    def test_task_v0_create(self):
        data = {
            'name': 'test',
        }
        resp = self.client.post('/task/v0/create', json=data)
        resp = resp.json()
        assert resp['code'] == 0

'''
locust -f test.py --host http://0.0.0.0:5000 --web-host 0.0.0.0
网页打开浏览器: http://0.0.0.0:8089
'''