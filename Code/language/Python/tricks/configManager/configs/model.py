# coding: utf-8
# Author: wanhui0729@gmail.com

_base_ = './model_base.py'

model = dict(
    device="cuda",
    backbone=dict(
        in_channels=3
    )
)