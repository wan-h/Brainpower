# coding: utf-8
# Author: wanhui0729@gmail.com

import time
import os, sys
import base64
import json
import cv2
import numpy as np
import requests
from io import BytesIO

root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)
from image_server import app
from fastapi.testclient import TestClient

# 初始化测试 client
c_client = TestClient(app)

image_path = os.path.join(root_path, 'test.jpg')

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
    ndarray_bytes = image_ndarray.tobytes()
    resp = c_client.post(url=url, params={'shape': json.dumps(shape)}, files={'file': ndarray_bytes})
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
    image_stream = open(image_path, 'rb')
    resp = c_client.post(url=url, files={'file': image_stream})
    res_data = resp.json()
    print(res_data)

def test_files_api():
    url = "/images/files/1"
    print(url)
    files = [('files', (open(image_path, 'rb'))), (('files', open(image_path, 'rb')))]
    resp = c_client.post(url=url, files=files)
    res_data = resp.json()
    print(res_data)

# 需要先启动server
def test_files_by_requests_api():
    url = "http://0.0.0.0:5000/images/files/"
    print(url)
    files = [('files', (open(image_path, 'rb'))), (('files', open(image_path, 'rb')))]
    resp = requests.post(url=url, files=files)
    res_data = resp.json()
    print(res_data)

T = 3
if __name__ == '__main__':
    times = []
    for _ in range(T):
        start = time.time()
        # test_base64_api()
        # test_file_api()
        # test_numpy_api()
        # test_files_api()
        test_files_by_requests_api()
        end = time.time()
        times.append(end - start)
    ave_time = np.mean(sorted(times)[1:-1])
    print(f"Ave time: {ave_time}")