# coding: utf-8
# Author: wanhui0729@gmail.com

"""
AMP用于使用双精度(FP32 FP16)混合训练，主要作用在于减少显存占用以及加快训练和推理速度
（只有部分显卡支持FP16）
* 实现细节：
网络前向计算过程中，权重、激活值和梯度都使用fp16进行存储，同时保留一份fp32的权重副本用于进行参数更新
使用fp32权重副本是因为bp更新梯度是一个很小的数字，很容易导致舍入误差(太小的梯度在fp32上有差异，但是到fp16相当于同一个值)
虽然保存了fp32的权重副本，但是内存占据任然能够减半，因为主要占据空间的是激活值(bp计算时使用)的存储，然而激活值的存储是使用fp16
* 其运算流程为：
Master-Weight(F32) -> Weights(F16) -> Weight Grad(F16) -> Update Master-Weights(F32)
FP直接使用F32的权重进行计算(auto_cast会自动将F32转为F16), 计算过程中得到的激活值使用F16进行存储
BP时先将权重float2half转为F16，然后通过链式法则计算梯度F16，权重更新时直接将梯度(还要乘一个学习率，所以这个值可能会导致F16下溢出)更新到F32的权重上
"""
from .visualizing import Net
from torch.cuda import amp
from torch import optim

model = Net().cuda()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 创建一个GrandScaler
scaler = amp.GradScaler()

# 假设变量
epochs = range(100)
data = (0, 0)
def loss_fn(output, taregt):
    pass

for epoch in epochs:
    for input, taregt in data:
        optimizer.zero_grad()

        # FP,autocast自动将梯度转为F16
        with amp.autocast():
            # input为F16
            output = model(input)
            loss = loss_fn(output, taregt)
        # scaler将loss进行的放大
        # 主要作用是保证BP的计算过程中不会产生下溢出，因为BP的计算都是Fp16的计算
        scaler.scale(loss).backward()
        # 更新weight,在更新weight之前会现将梯度unscale回去
        # 如果有inf/NaN的Grad会忽略本次更新
        scaler.step(optimizer)
        # 进入下一次迭代
        scaler.update()