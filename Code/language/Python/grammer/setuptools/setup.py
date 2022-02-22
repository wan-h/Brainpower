"""
# 构建方法
pip install build
python -m build
# 不在独立的虚拟环境中构建，因为会有一些依赖
python -m build -n
# 执行后会产生tar.gz和.whl文件，这些文件可以上传发布到PyPI了
# .tar.gz只有配置进去的文件，.whl会包含扩展编译的文件.so

# 本地安装
python setup.py install

#相关参数定义可以参考网址
https://docs.python.org/3/distutils/apiref.html
"""

import os
import glob
from setuptools import setup
from setuptools import find_packages
# from setuptools import Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

# 混合编译，获取扩展模块
def get_extensions():
    pwd_dir = os.path.dirname(os.path.abspath(__file__))
    extensions_dir = os.path.join(pwd_dir, "src", "additional", "csrc")
    # cpp源代码文件, main_file是基于pybind的封装接口
    main_file = glob.glob(os.path.join(extensions_dir, "*.cpp"))
    sources_cpu = glob.glob(os.path.join(extensions_dir, "cpu", "*.cpp"))
    sources = main_file + sources_cpu
    # 头文件路径
    include_dirs = [os.path.join(extensions_dir, 'include')]
    # 宏定义
    # 以下定义相当于：
    #   #define DEBUG 1
    #   #define LOG
    #   #undef DEBUG
    define_macros = [('DEBUG', '1'), ('LOG', None)]
    undef_macros = ['DEBUG']
    # 编译参数
    # extra_compile_args = {"cxx": []}

    # 构建扩展模块
    ext_modules = [
        Pybind11Extension(
            # 扩展包名,放到模块中才能import到, 对应hello.py中的import位置
            name="pkg1._C",
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            undef_macros=undef_macros,
            # extra_compile_args=extra_compile_args,
        )
    ]
    return ext_modules

setup(
    # 包名称
    name='mypackage',
    # 包版本
    version='0.0.1',
    author='wanh',
    author_email="13658247573@163.com",
    # 程序官网
    url="https://...",
    license="MIT",
    #项目简短描述，会显示在 PyPI 上名字下端
    description="This is a sample package",
    # 所有的数据文件都会包含进安装包中
    include_package_data=False,
    # 指定数据文件
    package_data={
        # 任何包里面包含以下类型文件都会放进安装包
        "": ["*.txt", "*.rst"],
        # pkg1模块中的以下类型文件将会放进安装包，支持模块中的子目录
        "pkg1": [".msg", "data/*.dat"],
    },
    # 筛选掉不需要的文件放进安装包
    exclude_package_data={"": ["README.txt"]},
    # packages = ['pkg1'],
    packages=find_packages(
        # 默认是当前目录，即在该指定的目录下搜索模块
        where='src',
        # 匹配需要包含的模块名
        include=['pkg*', 'additional'],
        # 筛选掉不需要包含的模块
        # exclude=['additional'],
    ),
    # 告诉setuptools所有的包都在src目录下，这个需要和packages下的模块列表一一对应
    # 安装后每一个包都可以被单独import, "import pkg1, import pkg2"
    # 不推荐这种写法，只需要一个主模块然后packages=find_packages()即可，package_dir也不需要写
    package_dir={"": "src"},
    #指定项目依赖的 Python 版本
    python_requires='>=3',
    # 安装依赖，在安装包的时候会下载依赖进行安装
    # install_requires=['Flask>=0.10'],
    # 依赖包下载路径:路径指向egg包，也可是包下载地址的页面
    # dependency_links=['http://example.com/dependency.tar.gz'],
    # 构建自定义行为的构建模块(编译C++), 这里使用pybind11的来构建python接口
    ext_modules=get_extensions(),
    cmdclass={"build_ext": build_ext},
)