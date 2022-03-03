# coding: utf-8
# Author: wanhui0729@gmail.com

# https://github.com/pybind/python_example

# first step: pip install ./class_example

import class_example

if __name__ == '__main__':
    # 这个doc就是在main.cpp中定义的模块doc
    print("="* 100 + '\n', class_example.__doc__)
    # 这个doc就是在main.cpp中定义的类doc
    print("=" * 100 + '\n', class_example.Pet.__doc__)
    # 使用类
    pet = class_example.Pet("Niuniu", class_example.Pet.Dog)
    print("=" * 100 + '\n', pet)
    print("=" * 100 + '\n', pet.name)
    pet.setName("Jiji")
    print("=" * 100 + '\n', pet.getName())
    # age是私有成员
    pet.age = 10
    print("=" * 100 + '\n', pet.age)
    # 动态属性，相当于在python对象的__dict__中添加属性
    pet.gender = "girl"
    print("=" * 100 + '\n', pet.__dict__)

    # 调用继承类
    dog = class_example.Dog("wangcai", class_example.Pet.Dog)
    print("=" * 100 + '\n', dog.go())

    # 多态，虽然main.cpp中智能指正指向的是一个Pet基类，但是获取到的对象是一个派生类，pybind11会检测到虚函数后自动将其视为多态
    dog = class_example.pet_store()
    print("=" * 100 + '\n', type(dog))
    print("=" * 100 + '\n', dog.go())

    # 重载函数
    dog.set(21)
    print("=" * 100 + '\n', dog.age)

    # 获取结构体变量
    print("=" * 100 + '\n', dog.attr.gender)