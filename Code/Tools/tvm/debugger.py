# -*- coding: utf-8 -*-
# @Author  : wanhui

"""
https://tvm.apache.org/docs/arch/debugger.html
"""

import tvm
import onnx
import numpy as np
from PIL import Image
import tvm.relay as relay
from tvm.contrib.download import download_testdata
from tvm.contrib import graph_executor
from tvm.contrib.debugger.debug_executor import GraphModuleDebug

def get_debug_output():
    """
    Downloading and Loading the ONNX Model
    """
    print("=" * 50 + "Downloading and Loading the ONNX Model" + "=" * 50)
    model_url = (
        "https://github.com/onnx/models/raw/main/"
        "vision/classification/resnet/model/"
        "resnet50-v2-7.onnx"
    )

    # 下载太慢了
    # model_path = download_testdata(model_url, "resnet50-v2-7.onnx", module="onnx")
    model_path = "resnet50-v2-7.onnx"
    onnx_model = onnx.load(model_path)



    """
    Downloading, Preprocessing, and Loading the Test Image
    """
    print("=" * 50 + "Downloading, Preprocessing, and Loading the Test Image" + "=" * 50)
    # img_url = "https://s3.amazonaws.com/model-server/inputs/kitten.jpg"
    # img_path = download_testdata(img_url, "kitten.jpg", module="data")
    img_path = "kitten.jpg"
    # resize
    resized_image = Image.open(img_path).resize((224, 224))
    img_data = np.asarray(resized_image).astype("float32")
    # HWC -> CHW for onnx
    img_data = np.transpose(img_data, (2, 0, 1))
    # 输入归一化
    imagenet_mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
    imagenet_stddev = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
    norm_img_data = (img_data / 255 - imagenet_mean) / imagenet_stddev
    # 扩展batch维度
    img_data = np.expand_dims(norm_img_data, axis=0)



    """
    Compile the Model With Relay
    """
    print("=" * 50 + "Compile the Model With Relay" + "=" * 50)
    target = "llvm"
    input_name = "data"
    shape_dict = {input_name: img_data.shape}

    mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

    with tvm.transform.PassContext(opt_level=3):
        lib = relay.build(mod, target=target, params=params)
    # 存储模型，避免重复Build
    lib.export_library('model.so')



    """
    Load the Model and get debug output
    """
    # 直接获取存储的so库
    # lib = tvm.runtime.load_module("model.so")
    # 获取tvm运行设备
    dev = tvm.device(str('llvm'), 0)

    # 对应加载so库获取图执行器的方法
    # m = graph_executor.create(lib["get_graph_json"](), lib, dev, dump_root="/tmp/tvmdbg")

    module = GraphModuleDebug(
        lib["debug_create"]("default", dev),
        [dev],
        lib.graph_json,
        dump_root="/tmp/tvmdbg",
    )

    print("=" * 50 + "Execute on the TVM Runtime" + "=" * 50)
    dtype = "float32"
    module.set_input(input_name, img_data)
    module.run()
    output_shape = (1, 1000)
    # tvm.nd就是tvm的ndarray
    tvm_output = module.get_output(0, tvm.nd.empty(output_shape)).numpy()

def get_output_tensor():
    with open("tvmdbg/output_tensors.params", "rb") as f:
        params = bytearray(f.read())
    params_dict = tvm.relay.load_param_dict(params)
    for k, v in params_dict.items():
        if 'tvmgen_default_fused_nn_max_pool2d_multiply_add_nn_relu' in k:
        
            print("name", k)
            print("shape:", v.shape)


if __name__ == "__main__":
    # get_debug_output()
    get_output_tensor()
