# 生成MathFunction库文件
add_library(MathFunctions mysqrt.cpp)

# 表示任何需要链接到该库的目标需要包含该资源目录找到 .h 文件
target_include_directories(MathFunctions
    INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
    )

# 安装规则
install(TARGETS MathFunctions DESTINATION lib)
install(FILES MathFunctions.h DESTINATION include)