# coding: utf-8
# Author: wanhui0729@gmail.com

import time
import os, sys
import base64
import json
import cv2
import numpy as np
from io import BytesIO

root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)
from image_server import app
from fastapi.testclient import TestClient

# 初始化测试 client
c_client = TestClient(app)

# image_path = os.path.join(root_path, 'test.jpg')
# image_path = os.path.join(root_path, '512.png')
# image_path = os.path.join(root_path, '1080P.png')
image_path = os.path.join(root_path, '2K.png')
# image_path = os.path.join(root_path, '4K.png')

def test_base64_api():
    url = "/images/base64/1"
    print(url)
    with open(image_path, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data)
    image_str = base64_data.decode()
    resp = c_client.post(url=url, json={'images': [image_str]})
    res_data = resp.json()
    print(res_data)

def test_numpy_api():
    url = "/images/numpy/1"
    print(url)
    image_ndarray = cv2.imread(image_path)
    shape = image_ndarray.shape
    resp = c_client.post(url=url, params={'shape': json.dumps(shape)}, files={'file': image_ndarray.tobytes()})
    res_data = resp.json()
    print(res_data)

"""
！！！
依赖安装
pip install python-multipart
"""
def test_file_api():
    url = "/images/file/1"
    print(url)
    resp = c_client.post(url=url, files={'file': open(image_path, 'rb')})
    res_data = resp.json()
    print(res_data)

T = 10
if __name__ == '__main__':
    times = []
    for _ in range(T):
        start = time.time()
        test_base64_api()
        # test_file_api()
        # test_numpy_api()
        end = time.time()
        times.append(end - start)
    ave_time = np.mean(sorted(times)[1:-1])
    print(f"Ave time: {ave_time}")