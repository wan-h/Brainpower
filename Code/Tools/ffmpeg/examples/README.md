# 环境准备  
[ffmpeg编译参考文档](https://j6sc416eds.feishu.cn/docx/doxcnDfFEQiyzgBsQxMIT8N4jWe)  
修改CMakeLists包含头文件和lib库  
`使用静态库避免出现SB问题需要链接很多库`
# 编译
```
mkdir build
cd build

# linux
cmake .. 
# windows
cmake -G "MinGW Makefiles" ..

make
```