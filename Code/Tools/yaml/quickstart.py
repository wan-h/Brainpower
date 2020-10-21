# coding: utf-8
# Author: wanhui0729@gmail.com

import os
import yaml
from yacs.config import CfgNode as CN


yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.yaml')
def yaml_parse():
    with open(yaml_path, 'r') as f:
        # 解析yaml文件为字典
        data = yaml.load(f)
    print("="*21)
    print("Get yaml data: ")
    print(data)

def yacs_parse():
    '''
    通过节点管理配置参数
    '''
    cfg = CN()

    cfg.USER = CN()
    cfg.USER.NAME = ''
    cfg.USER.AGE = 0

    cfg.USER.COMM = CN()
    cfg.USER.COMM.PHONE = 123
    cfg.USER.COMM.EMAIL = ''

    print("=" * 21)
    # 从文件合并
    cfg.merge_from_file(yaml_path)
    print("Get yacs data from file: ")
    print(cfg)
    # 从列表合并,修改相应字段
    merge_list = ['USER.NAME', 'test2']
    cfg.merge_from_list(merge_list)
    print("Change data from list: ")
    print(cfg.USER.NAME)

if __name__ == '__main__':
    yaml_parse()
    yacs_parse()