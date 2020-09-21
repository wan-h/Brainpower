# coding: utf-8
# Author: wanhui0729@gmail.com

import cv2
import time
import grpc
import tensorTransfer_pb2
import tensorTransfer_pb2_grpc
import numpy as np

SERVER_ADDRESS = "localhost:23333"

def simple_method(stub):
    print("--------------Call SimpleMethod Begin--------------")
    # image = cv2.imread('/home/wanh/workspace/image-test/4K.png')
    image = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.uint8)
    request = tensorTransfer_pb2.Request(
        shape=image.shape,
        data=image.data.tobytes(),
    )
    response = stub.SimpleMethod(request)
    print(response.message)
    print("--------------Call SimpleMethod Over---------------")

def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = tensorTransfer_pb2_grpc.tensorTransferStub(channel)
        simple_method(stub)

T = 10
if __name__ == '__main__':
    times = []
    for _ in range(T):
        start = time.time()
        main()
        end = time.time()
        times.append(end - start)
    ave_time = np.mean(sorted(times)[1:-1])
    print(f"Ave time: {ave_time}")