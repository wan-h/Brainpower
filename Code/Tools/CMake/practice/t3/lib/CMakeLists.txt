set(LIBHELLO_SRC hello.c)
# SHARED 动态库
add_library(hello SHARED ${LIBHELLO_SRC})
# STAIC 静态库, hello target只能存在一个，shared已经使用，所以这里换一个名字
add_library(hello_static STATIC ${LIBHELLO_SRC})
# 通过设置目标属性来解决名字冲突问题
set_target_properties(hello_static PROPERTIES OUTPUT_NAME "hello")

# 获取目标属性
get_target_property(OUTPUT_VALUE hello_static OUTPUT_NAME)
message(STATUS "This is the hello_static OUTPUT_NAME: " ${OUTPUT_VALUE})

# 设置版本号,VERSION 指代动态库版本,SOVERSION 指代 API 版本
set_target_properties(hello PROPERTIES VERSION 1.2 SOVERSION 1)

# ARCHIVE 特指静态库,LIBRARY 特指动态库
install(TARGETS hello hello_static
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib)
install(FILES hello.h DESTINATION include/hello)


# cmake -DCMAKE_INSTALL_PREFIX=/usr ..
# make
# make install