add_executable(main main.c)
# hello.h头文件搜索路径
include_directories(/usr/include/hello)
# main链接到libhello
# 链接动态库
# target_link_libraries(main libhello.so)
# 链接静态库
target_link_libraries(main libhello.a)