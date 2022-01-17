# coding: utf-8
# Author: wanhui0729@gmail.com

"""
需要一个中间文件做转换
pytorch -> onnx -> trt
pytorch -> caffe -> trt
"""

# import torch
# import torchvision
# import onnx

"""
将pytorch模型转换为onnx模型
"""
# def gen_onnx():
#     dummy_input = torch.randn(1, 3, 224, 224, device="cuda")
#     model = torchvision.models.resnet18(pretrained=True).cuda()
#     # 导出onnx模型
#     input_name = ["input"]
#     output_name = ["output"]
#     torch.onnx.export(model, dummy_input, "resnet18.onnx", input_names=input_name, output_names=output_name)
#     # 测试onnx文件
#     test = onnx.load("resnet18.onnx")
#     onnx.checker.check_model(test)

"""
使用tensorRT
使用镜像避免环境问题：docker pull venalone/tensorrt7:cuda10.2
安装过程：
$ conda install pycuda
$ pip install nvidia-pyindex
$ pip install nvidia-tensorrt
"""
import pycuda.autoinit
import pycuda.driver as cuda
import tensorrt as trt
import numpy as np
from PIL import Image

EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)

def GiB(val):
    return val * 1 << 30

# Simple helper data class that's a little nicer to use than a 2-tuple.
class HostDeviceMem(object):
    def __init__(self, host_mem, device_mem):
        self.host = host_mem
        self.device = device_mem

    def __str__(self):
        return "Host:\n" + str(self.host) + "\nDevice:\n" + str(self.device)

    def __repr__(self):
        return self.__str__()


# Allocates all buffers required for an engine, i.e. host/device inputs/outputs.
def allocate_buffers(engine):
    inputs = []
    outputs = []
    bindings = []
    stream = cuda.Stream()
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        # Allocate host and device buffers
        host_mem = cuda.pagelocked_empty(size, dtype)
        device_mem = cuda.mem_alloc(host_mem.nbytes)
        # Append the device buffer to device bindings.
        bindings.append(int(device_mem))
        # Append to the appropriate list.
        if engine.binding_is_input(binding):
            inputs.append(HostDeviceMem(host_mem, device_mem))
        else:
            outputs.append(HostDeviceMem(host_mem, device_mem))
    return inputs, outputs, bindings, stream


# This function is generalized for multiple inputs/outputs.
# inputs and outputs are expected to be lists of HostDeviceMem objects.
def do_inference(context, bindings, inputs, outputs, stream, batch_size=1):
    # Transfer input data to the GPU.
    [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]
    # Run inference.
    context.execute_async(batch_size=batch_size, bindings=bindings, stream_handle=stream.handle)
    # Transfer predictions back from the GPU.
    [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
    # Synchronize the stream
    stream.synchronize()
    # Return only the host outputs.
    return [out.host for out in outputs]


# This function is generalized for multiple inputs/outputs for full dimension networks.
# inputs and outputs are expected to be lists of HostDeviceMem objects.
def do_inference_v2(context, bindings, inputs, outputs, stream):
    # Transfer input data to the GPU.
    [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]
    # Run inference.
    context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
    # Transfer predictions back from the GPU.
    [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
    # Synchronize the stream
    stream.synchronize()
    # Return only the host outputs.
    return [out.host for out in outputs]


class ModelData():
    MODEL_PATH = "resnet18.onnx"
    INPUT_SHAPE = (3, 224, 224)
    DTYPE = trt.float32

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

# 生成tensorrt engine文件
def build_engine_onnx(model_file):
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(EXPLICIT_BATCH)
    config = builder.create_builder_config()
    parser = trt.OnnxParser(network, TRT_LOGGER)
    # 给出模型中任一层能使用的内存上限 1G
    config.max_workspace_size = GiB(1)

    with open(model_file, 'rb') as model:
        if not parser.parse(model.read()):
            print("ERROR: Failed to parse the ONNX file.")
            for error in range(parser.num_errors):
                print(parser.get_error(error))
            return None
    return builder.build_engine(network, config)

def load_normalized_test_case(test_image, pagelocked_buffer):
    # Converts the input image to a CHW Numpy array
    def normalize_image(image):
        # Resize, antialias and transpose the image to CHW.
        c, h, w = ModelData.INPUT_SHAPE
        image_arr = np.asarray(image.resize((w, h), Image.ANTIALIAS)).transpose([2, 0, 1]).astype(
            trt.nptype(ModelData.DTYPE)).ravel()
        # This particular ResNet50 model requires some preprocessing, specifically, mean normalization.
        return (image_arr / 255.0 - 0.45) / 0.225

    # Normalize the image and copy to pagelocked memory.
    np.copyto(pagelocked_buffer, normalize_image(Image.open(test_image)))
    return test_image

def main():
    test_image = np.random.randint(0, 255, [3, 224, 224])

    engine = build_engine_onnx(ModelData.MODEL_PATH)

    inputs, outputs, bindings, stream = allocate_buffers(engine)
    # Contexts are used to perform inference.
    context = engine.create_execution_context()

    # load_normalized_test_case(test_image, inputs[0].host)
    trt_outputs = do_inference_v2(context, bindings, inputs, outputs, stream)

    print(trt_outputs)

if __name__ == '__main__':
    # gen_onnx()
    main()