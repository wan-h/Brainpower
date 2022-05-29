cmake_minimum_required(VERSION 2.8)

project("thread_mgr")

# 启动断言assert
add_definitions(-DMY_DEBUG=1)

include_directories(${CMAKE_SOURCE_DIR}/include)
file(GLOB SRC ${CMAKE_SOURCE_DIR}/src/*.cpp)

add_executable(main main.cpp ${SRC})