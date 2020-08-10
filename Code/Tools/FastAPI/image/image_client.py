# coding: utf-8
# Author: wanhui0729@gmail.com

import os, sys
import base64
import json

root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from image_server import app
from fastapi.testclient import TestClient

# 初始化测试 client
c_client = TestClient(app)

image_path = os.path.join(root_path, 'test.jpg')

if __name__ == '__main__':
    url = "/images/1"
    with open(image_path, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data)
    image_str = base64_data.decode()
    resp = c_client.post(url=url, json={'images': [image_str]})
    res_data = resp.json()
    print(res_data)