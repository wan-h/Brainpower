cmake_minimum_required(VERSION 3.10)

# 设置项目名字和版本
project(Detector VERSION 1.0)

# 设置ncnn安装位置
set(NCNN_INSTALL "/home/wan/workspace/code/ncnn/build/install")

# 调用opencv
find_package(OpenCV REQUIRED)
# 调用openmp
find_package(OpenMP REQUIRED)  
if(OPENMP_FOUND)  
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")  
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")  
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")  
endif()


# 包含ncnn的头文件
include_directories(${NCNN_INSTALL}/include/ncnn)
# 包含ncnn的链接文件
link_directories(${NCNN_INSTALL}/lib)
message(STATUS "NCNN library: ${NCNN_INSTALL}")

# 生成可执行文件
add_executable(detector Detector.cpp)
target_include_directories(detector PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(detector PRIVATE ncnn ${OpenCV_LIBS})