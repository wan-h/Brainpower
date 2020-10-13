# coding: utf-8
# Author: wanhui0729@gmail.com

import pytest

def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4

"""
pytest test_sample_1.py
"""
# 或则使用pytest.mian
if __name__ == '__main__':
    pytest.main(['-s', 'test_sample_1.py'])