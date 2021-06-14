cmake_minimum_required(VERSION 3.10)

# 设置项目名字和版本
project(Tutorial VERSION 2.1)

# 指定c++标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 设置cmake选项控制编译
# 使用示例： cmake .. -DUSE_MYMATH=ON
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# 将CMake中的一些设置配置成源代码中的一个头文件，该头文件会生成到CMake二进制目录中 ${PROJECT_BINARY_DIR}
configure_file(TutorialConfig.h.in TutorialConfig.h)

# 增加MathFunctions库
if(USE_MYMATH)
    # 添加 MathFunctions 子目录并构建该子目录
    add_subdirectory(MathFunctions)
    # 构建EXTRA_LIBS列表
    list(APPEND EXTRA_LIBS MathFunctions)
    # 构建EXTRA_INCLUDES列表
    # list(APPEND EXTRA_INCLUDES "${PROJECT_SOURCE_DIR}/MathFunctions")
endif()

# 生成一个可执行文件
add_executable(Tutorial tutorial.cpp)
# 目标文件与库文件进行链接
target_link_libraries(Tutorial PUBLIC ${EXTRA_LIBS})


# 增加CMake二进制目录到头文件的搜索路径中，因为configure_file生成的头文件在该路径下
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                        #    ${EXTRA_INCLUDES}
                           )
