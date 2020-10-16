# coding: utf-8
# Author: wanhui0729@gmail.com

import os
import yaml
import logging.config

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')


# 通过配置文件构建logger
if __name__ == '__main__':
    with open(config_path, 'r') as f:
        config = yaml.load(f)
        # 加载配置字典，json也可以存储字典结构
        logging.config.dictConfig(config)

    # 获取root logger
    logger = logging.getLogger()
    # 效果同quickStart.py
    logger.debug("test debug msg")
    logger.info("test info msg")
    logger.error("test error msg")

    print("*" * 10 + 'test logger' + "*" * 10)
    # 配置文件中设置的logger
    logger = logging.getLogger('test')
    # 未达到root基础过滤级别
    logger.debug("test debug msg")
    logger.info("test info msg")
    logger.error("test error msg")