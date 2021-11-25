# coding: utf-8
# Author: wanhui0729@gmail.com

from fabric.api import *

# 使用本机ip虚拟远程访问
LOCAL_IP = "wanh@127.0.0.1"
HOST_IP = "wanh@172.31.3.137"
HOST_PW = "123456"

# 定义角色
env.roledefs = {
    "myserver1": [HOST_IP],
    "myserver2": [LOCAL_IP]
}

# 定义服务器密码
# 密码的key是host strings的全称，user@ip:port
env.passwords = {
    "{}:22".format(HOST_IP): HOST_PW,
    "{}:22".format(LOCAL_IP): HOST_PW,
}

# run执行服务器命令
# cd 进入服务器目录
@roles("myserver1")
def my_func_1():
    print("Executing on %s as %s" % (env.host, env.user))
    with cd("~"):
        ret = run("ls")
    print("Executing output: {}".format(ret))

@roles("myserver2")
def my_func_2():
    print("Executing on %s as %s" % (env.host, env.user))
    with cd("~"):
        ret = run("ls")
    print("Executing output: {}".format(ret))

# fab -f quickStart.py task
def task():
    execute(my_func_1)
    execute(my_func_2)