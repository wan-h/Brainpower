# coding: utf-8
# Author: wanhui0729@gmail.com

'''
fixture使用autouse就会在scope范围内自动使用
'''
import pytest

@pytest.fixture(scope='class', autouse=True)
def hello_class():
    print("\nhello class")

@pytest.fixture(scope='function', autouse=True)
def hello_function():
    print("\nhello function")

# @pytest.mark.usefixtures('hello_class')
# @pytest.mark.usefixtures('hello_function')
class TestCase(object):
    def test_1(self):
        print("----------test_1-----------")
    def test_2(self):
        print("----------test_2-----------")

if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture_2.py'])