# coding: utf-8
# Author: wanhui0729@gmail.com

import time

class Timer(object):
    def __init__(self, tag):
        self.tag = tag
        self.diff = 0

    def get_diff(self):
        return self.end_time - self.start_time

    def __enter__(self):
        self.start_time = time.time()
        return self.get_diff

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        diff_time = self.end_time - self.start_time
        print("{}: {}".format(self.tag, diff_time))


if __name__ == '__main__':
    with Timer("Test cost") as t:
        time.sleep(1)
    print(t())