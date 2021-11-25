project(HELLO)
# 向当前工程添加存放源文件的子目录,并可以指定中间二进制和目标二进制存放的位置
# 该命令设置EXECUTABLE_OUTPUT_PATH 和 LIBRARY_OUTPUT_PATH 变量来指定最终的目标二进制的位置
add_subdirectory(src bin)
# 安装 COPYRIGHT/README
install(FILES COPYRIGHT README DESTINATION share/doc/cmake/t2)
# 安装 runhello.sh
install(PROGRAMS runhello.sh DESTINATION bin)
# 安装 doc 中的 hello.txt
# DIRECTORY 后面连接的是所在 Source 目录的相对路径
# 如果目录名不以/结尾,那么这个目录将被安装为目标路径下的 abc,如果目录名以/结尾,代表将这个目录中的内容安装到目标路径
install(DIRECTORY doc/ DESTINATION share/doc/cmake/t2)



# make install 安装时使用参数指定安装目录
# CMAKE_INSTALL_PREFIX 的默认定义是/usr/local
# cmake -DCMAKE_INSTALL_PREFIX=/tmp/t2/usr ..