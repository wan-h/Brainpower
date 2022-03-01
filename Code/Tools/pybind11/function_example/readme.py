# coding: utf-8
# Author: wanhui0729@gmail.com

# https://github.com/pybind/python_example

# first step: pip install ./function_example

import function_example

if __name__ == '__main__':
    # 这个doc就是在main.cpp中定义的doc
    print("="* 100 + '\n', function_example.__doc__)
    # 会显示默认参数等
    print("=" * 100 + '\n', function_example.add.__doc__)
    # 没有doc的基本只有函数名字显示
    print("=" * 100 + '\n', function_example.generic.__doc__)
    print("="* 100 + '\n', function_example.add())
    print("=" * 100 + '\n', function_example.add(i=3, j=5))
    print("=" * 100 + '\n')
    # 传递python字典
    data = {"test": "for test"}
    # c++端调用了打印
    function_example.print_dict(data)
    print("=" * 100 + '\n')
    # 解析**kwargs参数
    function_example.generic(a=12, b=13)