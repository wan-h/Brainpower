# coding: utf-8
# Author: wanhui0729@gmail.com

import grpc
import tensorTransfer_pb2
import tensorTransfer_pb2_grpc
from concurrent import futures
import numpy as np
import cv2

__all__ = 'TensorTransfer'
SERVER_ADDRESS = 'localhost:23333'

class TensorTransfer(tensorTransfer_pb2_grpc.tensorTransferServicer):
    def SimpleMethod(self, request, context):
        shape = request.shape
        data = request.data
        tensor_flatten = np.frombuffer(data, np.uint8)
        tensor = tensor_flatten.reshape(shape)
        reponse = tensorTransfer_pb2.Reponse(
            message='Get data successfully!'
        )
        return reponse


MAX_MESSAGE_LENGTH = 1024*1024*1024  # 修改传输限制
def main():
    server = grpc.server(futures.ThreadPoolExecutor(), options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
    ])
    tensorTransfer_pb2_grpc.add_tensorTransferServicer_to_server(TensorTransfer(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    print("------------------start Python GRPC server")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    main()