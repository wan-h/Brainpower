# coding: utf-8
# Author: wanhui0729@gmail.com

import torch
from torch.quantization import prepare_qat, get_default_qat_qconfig, convert
from torchvision.models import quantization

# Step1: 修改模型, 这里直接使用官方提供的
"""
1. FP前面加上量化模块，将输入量化到int8, 最后加上反量化模块，将输出反量化到fp32
def forward(self, x):
    x = self.quant(x)
    x = self._forward_impl(x)
    x = self.dequant(x)
    return x

2. 对于加法加入伪量化节点，因为int8数值进行加法运算容易超出数值范围，所以不是直接进行计算，而是进行反量化->计算->量化的操作
self.skip_add = nn.quantized.FloatFunctional()

3. 实现折叠函数
"""
model = quantization.mobilenet_v2()
print("original model:\n", model)

# Step2: 折叠算子，减少计算量和加速推理，减少中间计算过程的误差积累，因为每一个算子都需要量化和反量化
model.train()
model.fuse_model()
print("fused model:\n", model)

# Step3:指定量化方案
BACKEND = "fbgemm"
model.qconfig = get_default_qat_qconfig(BACKEND)

# Step4：插入伪量化模块
# 给每个层增加FakeQuantize()模块
prepare_qat(model, inplace=True)
print("model with observer:\n", model)

# Step5: 正常的模型训练，无需修改代码

# Step6：实施量化，获得量化后模型
model.eval()
# 执行convert函数前，需确保模型在evaluate模式
model_int8 = convert(model)
print("quantized model:\n", model_int8)

# Step6：int8模型推理
# 指定与qconfig相同的backend，在推理时使用正确的算子
torch.backends.quantized.engine = BACKEND
# 目前Pytorch的int8算子只支持CPU推理,需确保输入和模型都在CPU侧
# 输入输出仍为浮点数
fp32_input = torch.randn(1, 3, 224, 224)
y = model_int8(fp32_input)
print("output:\n", y)