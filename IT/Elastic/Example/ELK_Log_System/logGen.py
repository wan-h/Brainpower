# coding: utf-8
# Author: wanhui0729@gmail.com

import sys
import json
import time
import random
import logging

def genLog(logfile):
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    users = ['test01', 'test02', 'test03']
    while True:
        random_user = random.choice(users)
        random_number = random.randint(1, 10)
        info = {
            'user': random_user,
            'data': random_number
        }
        logger.info(json.dumps(info))
        time.sleep(1)
if __name__ == '__main__':
    log_file = '/home/wan/test.log'
    genLog(log_file)