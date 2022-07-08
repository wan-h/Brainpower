cmake_minimum_required(VERSION 2.8)

project("fzlog_example")

# 连接到ffmpeg头文件和库相关路径
include_directories(${CMAKE_SOURCE_DIR}/include)


add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} -lpthread)