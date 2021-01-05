# coding: utf-8
# Author: wanhui0729@gmail.com

from fabric.api import *

'''
安装支持python3.4+版本 pip install fabric3
fabfile.py 免导入Fabric API
直接在当前目录适应fab cmd执行，fab自动检测当前目录下的fabfile.py文件
'''

# fab hello_1
def hello_1():
    print("Hello world!")

# 参数传递
# fab hello_2:name=Wanh
def hello_2(name="world"):
    print("Hello %s!" % name)

# local执行本机命令
# lcd 进入本机目录
# fab hello_3
def cd_ls():
    with lcd("~"):
        local("ls")
def hello_3():
    cd_ls()
