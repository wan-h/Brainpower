# coding: utf-8
# Author: wanhui0729@gmail.com

"""
toml的解析接口和json是一致的
"""

import os
import toml

toml_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'example.toml')

if __name__ == '__main__':
    # 加载toml文件，获取到的是一个字典对象
    data_dict = toml.load(toml_path)
    print("=" * 100 + "\n", data_dict)
    # 将字典对象转换为字符串对象
    data_str = toml.dumps(data_dict)
    print("=" * 100 + "\n", data_str)
    # 将字符串对象转换为字典对象
    data_dict = toml.loads(data_str)
    print("=" * 100 + "\n", data_dict)
    # 将字典写入文件中
    with open("example_gen.toml", 'w') as f:
        toml.dump(data_dict, f)