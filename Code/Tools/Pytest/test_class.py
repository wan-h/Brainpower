# coding: utf-8
# Author: wanhui0729@gmail.com

class TestClass():
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")

"""
pytest -q test_class.py
"""