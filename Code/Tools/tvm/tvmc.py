# -*- coding: utf-8 -*-
# @Author  : wanhui

"""
https://tvm.apache.org/docs/tutorial/tvmc_python.html#
Getting Starting using TVMC Python: a high-level API for TVM
"""

from tvm.driver import tvmc
"""
tvmc是tvm的一个更加高级抽象的接口，内部自己封装了tvm的系列操作，详细操作需要看tvm的示例
"""
# load model
"""
wget https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet50-v2-7.onnx
tvmc.load的shape_dict在使用pytorch的时候必须指定该参数
model = tvmc.load(model, shape_dict={'input1' : [1, 2, 3, 4], 'input2' : [1, 2, 3, 4]})
"""
print("=" * 100 + 'Load Model' + "=" * 100)
model = tvmc.load('resnet50-v2-7.onnx')
# 保存Relay转换的文件
model.save('model.relay')

# Tune[Option](对模型进行加速优化调整)
"""
enable_autoscheduler自动生成优化搜索空间,该操作比较耗时
"""
# print("=" * 100 + 'Tune Model' + "=" * 100)
# tuning_records = tvmc.tune(model, target="llvm", enable_autoscheduler=True)
# 保存优化调整后的结果(其实就是再跑一下tune)
# tvmc.tune(model, target="llvm", tuning_records=tuning_records)

# Compile
"""
target指定编译器
* cuda (Nvidia GPU)
* llvm (CPU)
* llvm -mcpu=cascadelake (Intel CPU)
"""
print("=" * 100 + 'Compile Model' + "=" * 100)
# package_path指定将编译结果保存的输出文件
# package可以直接 tvmc.run(package)
package = tvmc.compile(model, target="llvm", package_path="model.package")


# Run
"""
device指定运行设备，和编译指定的编译器应该成一一对应关系
lg: CPU, Cuda, CL, Metal, and Vulkan
"""
print("=" * 100 + 'Run Model' + "=" * 100)
# 加载保存的编译文件
new_package = tvmc.TVMCPackage(package_path="model.package")
result = tvmc.run(new_package, device='cpu')
print(result)