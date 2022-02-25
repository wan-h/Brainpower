cmake_minimum_required(VERSION 3.4...3.18)
project(cmake_example)

# 需要在当前目录建一个软连接到pybind11，这样才能编译到pybind11
# pybind11中定义了pybind11_add_module cmake接口
add_subdirectory(pybind11)
# 这个接口大致应该是使用pybind11生成目标文件，类似add_executable来生成目标文件
pybind11_add_module(cmake_example src/main.cpp)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a define (VERSION_INFO) here.
target_compile_definitions(cmake_example PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})