# coding: utf-8
# Author: wanhui0729@gmail.com

import logging

'''
python logging 

* 日志级别
CRITICAL = FATAL > ERROR > WARNING > INFO > DEBUG
FATAL: 严重的错误事件将会导致应用程序的退出
ERROR: 虽然发生错误事件，但仍然不影响系统的继续运行
WARNING: 出现潜在错误
INFO: 突出强调应用程序的运行过程
DEBUG: 调试应用程序

* format
%(levelno)s：打印日志级别的数值
%(levelname)s：打印日志级别的名称
%(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s：打印当前执行程序名
%(funcName)s：打印日志的当前函数
%(lineno)d：打印日志的当前行号
%(asctime)s：打印日志的时间
%(thread)d：打印线程ID
%(threadName)s：打印线程名称
%(process)d：打印进程ID
%(message)s：打印日志信息
'''

def getLogger():
    logger = logging.getLogger('test')
    # 基础等级过滤，过滤掉级别低于INFO的
    logger.setLevel(logging.INFO)

    # 构建文件hander
    hander = logging.FileHandler('log.txt')
    # 在基础过滤的基础上再过滤掉级别低于ERROR的
    hander.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s  File '%(filename)s',line %(lineno)s  %(levelname)s: %(message)s")
    hander.setFormatter(formatter)
    logger.addHandler(hander)

    # 构建stdout hander
    hander = logging.StreamHandler()
    # 在基础过滤的基础上再过滤掉级别低于ERROR的
    hander.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s  File '%(filename)s',line %(lineno)s  %(levelname)s: %(message)s")
    hander.setFormatter(formatter)
    logger.addHandler(hander)

    return logger

def getLogger2():
    pass

# 通过代码构建logger
if __name__ == '__main__':
    logger = getLogger()
    # 等级低于基础过滤设置的等级，不会有任何输出
    logger.debug("test debug msg")
    # 等级高于基础过滤等级，高于stream过滤等级，低于文件过滤等级，所以只会在stdout中输出
    logger.warning("test warning msg")
    # 等级高于基础过滤等级，高于stream过滤等级，高于文件过滤等级，所以会在所有hander中输出
    logger.error("test error msg")
