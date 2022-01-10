# coding: utf-8
# Author: wanhui0729@gmail.com

# 引入该包时就将resnet vgg注册进MODELS,不可省略
from .resnet import ResNet
from .vgg import Vgg

__all__ = ["ResNet", "Vgg"]