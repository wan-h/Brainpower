# coding: utf-8
# Author: wanhui0729@gmail.com

import os
import sys
root_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(root_path)

from lib.models import BACKBONES

if __name__ == '__main__':
    # 注册进入BACKBONES的模块可以直接被使用
    print(BACKBONES.get('vgg'))
    print(BACKBONES.get('resnet'))