# coding: utf-8
# Author: wanhui0729@gmail.com

import torch
from torch import nn
from torch.nn import functional as F

class model(nn.Module):
    def __init__(self):
        super().__init__()
        self.A = nn.Conv2d(3, 64, 3, stride=1, padding=1)
        self.B = nn.Conv2d(64, 3, 3, stride=1, padding=1)
    def forward(self, x):
        x = self.A(x)
        x = self.B(x)
        return x


def get_loss(x):
    b = x / 2.0
    with torch.no_grad():
        c = x / 2.0
    target = torch.ones_like(x)
    # 正常反向传播
    # loss = F.mse_loss(b, target)
    # 无法正常反向传播，因为grad屏蔽掉了所有的梯度传播
    # loss = F.mse_loss(c, target)
    # 正常反向传播，其中c将被视为一个常数项，b正常的反向传播通路
    loss = F.mse_loss(b+c, target)
    return loss

if __name__ == '__main__':
    a = torch.randn((1, 3, 5, 5,))
    model = model()
    out = model(a)
    loss = get_loss(out)
    loss.backward()