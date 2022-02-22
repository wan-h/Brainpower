# coding: utf-8
# Author: wanhui0729@gmail.com

# 根据setup.py的配置，会在pkg1下面生成.so文件
from pkg1 import _C

hello = _C.hello