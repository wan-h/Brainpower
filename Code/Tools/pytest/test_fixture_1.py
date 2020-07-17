# coding: utf-8
# Author: wanhui0729@gmail.com

'''
fixture在可以实现setup teardown功能
可作为参数使用
'''
import pytest

@pytest.fixture()
def hello():
    return "hello"

@pytest.fixture()
def say_hello():
    print("\nhello")



def test_fixture_function1(hello):
    assert hello == 'hello'

@pytest.mark.usefixtures('say_hello')
def test_fixture_function2():
    print("\ntest pytest.mark.usefixtures")

if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture_1.py'])