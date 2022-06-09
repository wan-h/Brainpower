# 环境准备  
[ffmpeg编译参考文档](https://j6sc416eds.feishu.cn/docx/doxcnDfFEQiyzgBsQxMIT8N4jWe)  
修改CMakeLists包含头文件和lib库  
`使用静态库避免出现SB问题需要链接很多库`

# 编译
```bash
mkdir build
cd build

# linux
cmake .. 
# windows
cmake -G "MinGW Makefiles" ..

make
```

# 测试
## 环境准备
```bash
# 提供链接库位置
export LD_LIBRARY_PATH=/root/ffmpeg_build/lib/share_lib:$LD_LIBRARY_PATH
# 提供ffmpeg工具位置
export PATH=/mnt/c/code/wanhui/ffmpeg:$PATH
```

## 示例测试
> mp4_2_yuv420.cpp
```bash
# 解封装mp4为yuv裸流
./mp4toyuv420 [inputfile] [outputfile]
# ffplay验证裸流正确性
ffplay -pixel_format yuv420p -video_size 1920x1088 [outputfile]
```