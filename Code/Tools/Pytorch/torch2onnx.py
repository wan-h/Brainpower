# coding: utf-8
# Author: wanhui0729@gmail.com

import onnx
import torch
import torchvision
import onnxruntime as ort
import numpy as np

dummy_input = torch.randn(10, 3, 224, 224, device='cuda')
model = torchvision.models.alexnet(pretrained=True).cuda()



# 只作用于打印显示名字，对onnx结构节点本身不影响
input_names = ["actual_input_1"] + ["learned_%d" % i for i in range(16)]
output_names = ["output1"]
torch.onnx.export(model, dummy_input, "alexnet.onnx", verbose=True, input_names=input_names, output_names=output_names)

# 直接使用onnx加载
model = onnx.load('alexnet.onnx')
# 检查模型完整性
onnx.checker.check_model(model)
# 打印onnx结构信息
print(onnx.helper.printable_graph(model.graph))

# onnx runtime直接做推理
ort_session = ort.InferenceSession("alexnet.onnx")
outputs = ort_session.run(
    # output_names
    None,
    # input_feed
    {"actual_input_1": np.random.randn(10, 3, 224, 224).astype(np.float32)}
)
print(outputs)