cmake_minimum_required(VERSION 2.8)

project("ffmpeg_example")

# 连接到ffmpeg头文件和库相关路径
include_directories(/opt/ffmpeg_build/include)
link_directories(/opt/ffmpeg_build/lib/share_lib)

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

add_executable(rtsp2h264 rtsp_2_h264.cpp)
target_link_libraries(
    rtsp2h264
    -lavcodec
    -lavformat
    -lavutil
)

add_executable(yuv420tortsp yuv420_2_rtsp.cpp)
target_link_libraries(
    yuv420tortsp
    -lavcodec
    -lavformat
    -lavutil
)

add_executable(h264_2_mp4 h264_2_mp4.cpp)
target_link_libraries(
    h264_2_mp4
    -lavcodec
    -lavformat
    -lavutil
)