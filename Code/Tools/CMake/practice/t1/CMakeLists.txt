# 该条语句完成HELLO_BINARY_DIR HELLO_SOURCE_DIR变量赋值
project(HELLO)
set(SRC_LIST main.c)
message(STATUS "This is BINARY dir " ${HELLO_BINARY_DIR})
message(STATUS "This is SOURCE dir " ${HELLO_SOURCE_DIR})
add_executable(hello ${SRC_LIST})