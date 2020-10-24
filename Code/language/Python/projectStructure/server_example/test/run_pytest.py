# coding: utf-8
# Author: wanhui0729@gmail.com

import os, sys
import argparse
test_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(test_path)
# 库路径添加到环境变量
sys.path.append(project_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--target_file', default='')
    args = parser.parse_args()
    test_target_file = args.target_file

    # 删除项目中的所有.pyc缓存
    os.system(f'find {project_path} -name "*.pyc" | xargs rm -rf')

    # 执行测试命令
    if test_target_file:
        test_path = os.path.join(test_path, test_target_file)
    cmd = f'pytest -q {test_path}'
    print("+" * 50)
    print(f"Executing cmd {cmd}")
    os.system(cmd)
