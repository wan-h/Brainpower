# coding: utf-8
# Author: wanhui0729@gmail.com

"""
使用yaml管理配置
"""

import os
import sys
root_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(root_path)

import argparse
from lib.configs import cfg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Config Manager Test")
    # 配置文件参数
    parser.add_argument(
        "--config-file",
        default="",
        metavar="FILE",
        help="path to config file",
        type=str,
    )
    # 所有剩余的命令行参数都被收集到一个列表中 opts
    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )

    args = parser.parse_args()

    # 合并配置文件(优先级高于默认配置)
    cfg.merge_from_file(args.config_file)
    # 合并命令参数(优先级高于配置文件)
    print(args.opts)
    cfg.merge_from_list(args.opts)
    # 冻结配置信息，无法更改
    cfg.freeze()
    print("Running with config:\n{}".format(cfg))

"""
>>> python main_yaml.py --config-file="configs/model.yaml" MODEL.BACKBONE.IN_CHANNELS 6
['MODEL.BACKBONE.IN_CHANNELS', '6']
Running with config:
MODEL:
  BACKBONE:
    IN_CHANNELS: 6
  DEVICE: cuda
"""