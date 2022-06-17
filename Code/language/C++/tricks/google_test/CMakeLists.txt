# 参考https://google.github.io/googletest/quickstart-cmake.html

cmake_minimum_required(VERSION 3.14)
set(PRJ_NAME my_gtest)
project(${PRJ_NAME})

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)
add_subdirectory(unittest)