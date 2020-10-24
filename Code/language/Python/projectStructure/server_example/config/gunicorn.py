import multiprocessing

'''
文件参考
https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
'''

bind = '0.0.0.0:5000'
# code change reload while debug
reload = False
# 进程数
workers = 4
daemon = True
errorlog = '../logs/gunicorn_error.log'
log_level = 'info'
pidfile = '../gunicorn.pid'