# 参考https://google.github.io/googletest/quickstart-cmake.html

cmake_minimum_required(VERSION 3.14)
set(PRJ_NAME my_unitest)
project(${PRJ_NAME})

# GoogleTest requires at least C++11
set(CMAKE_CXX_STANDARD 11)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()


set(UT_ROOT_PATH ${PROJECT_SOURCE_DIR})
file(GLOB UT_SOURCE_FILES ${UT_ROOT_PATH}/*.cpp)

add_executable(
  ${PRJ_NAME}
  ${UT_SOURCE_FILES}
)
target_link_libraries(
  ${PRJ_NAME}
  gtest_main
)

# 让cmake的test runner发现包含在二进制文件中的测试部分
# 可以直接执行ctest
include(GoogleTest)
gtest_discover_tests(${PRJ_NAME})