# coding: utf-8
# Author: wanhui0729@gmail.com

# https://github.com/pybind/python_example

# first step: pip install ./python_example

import cmake_example

if __name__ == '__main__':
    # 这个doc就是在main.cpp中定义的doc
    print("="* 100 + '\n', cmake_example.__doc__)
    print("=" * 100 + '\n', cmake_example.add.__doc__)
    res = cmake_example.add(1, 2)
    print("="* 100 + '\n', res)