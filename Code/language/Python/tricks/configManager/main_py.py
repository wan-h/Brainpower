# coding: utf-8
# Author: wanhui0729@gmail.com

"""
使用py字典管理配置
"""

import os
import sys
root_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(root_path)

import argparse
from mmcv import Config, DictAction

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
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.'
    )

    args = parser.parse_args()

    # 合并配置文件(优先级高于默认配置)
    cfg = Config.fromfile(args.config_file)
    # 合并命令参数(优先级高于配置文件)
    if args.cfg_options is not None:
        print(args.cfg_options)
        cfg.merge_from_dict(args.cfg_options)
    print("Running with config:\n{}".format(cfg))

"""
>>> python main_py.py --config-file="configs/model.py" --cfg-options model.backbone.in_channels=6
{'model.backbone.in_channels': 6}
Running with config:
Config (path: configs/model.py): {'model': {'device': 'cuda', 'backbone': {'in_channels': 6}}}
"""