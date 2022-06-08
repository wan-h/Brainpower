cmake_minimum_required(VERSION 2.8)

project("ffmpeg_example")

# 连接到ffmpeg头文件和库相关路径
include_directories(${CMAKE_SOURCE_DIR}/../3rdparty/include)
link_directories(${CMAKE_SOURCE_DIR}/../3rdparty/lib)

message(${CMAKE_SOURCE_DIR}/../3rdparty/include)

# 避免常量指针和指针之间的一些转换报错
add_compile_options(-fpermissive)

add_executable(mp4toyuv420 mp4_2_yuv420.cpp)
# 指定链接库
target_link_libraries(
    mp4toyuv420
    -lavcodec
    -lavformat
    -lavutil
)