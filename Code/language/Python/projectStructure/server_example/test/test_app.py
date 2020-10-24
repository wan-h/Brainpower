# coding: utf-8
# Author: wanhui0729@gmail.com

import pytest
from bin.app import app
from lib.server.server_user import _getUserId
from lib.server.server_task import _getTaskId
from fastapi.testclient import TestClient

# 初始化测试 client
c_client = TestClient(app)

class Test_App():
    def test_user_v0_register(self):
        url = '/user/v0/register/'
        item = {
            'name': 'test',
            'phone': '123456'
        }
        resp = c_client.post(url, json=item)
        assert resp.status_code == 200  # 程序状态码： 成功
        resp = resp.json()
        assert resp['code'] == 0
        assert resp['data']['id'] == _getUserId(item['name'], item['phone'])

    def test_task_v0_create(self):
        url = '/task/v0/create/'
        item = {
            'name': 'test',
        }
        resp = c_client.post(url, json=item)
        assert resp.status_code == 200  # 程序状态码： 成功
        resp = resp.json()
        assert resp['code'] == 0
        assert resp['data']['id'] == _getTaskId(item['name'])

if __name__ == '__main__':
    pytest.main(["-s", "test_app.py"])