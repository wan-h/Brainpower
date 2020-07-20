# coding: utf-8
# Author: wanhui0729@gmail.com

import pytest

def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()

"""
pytest -q test_sysexit.py
"""