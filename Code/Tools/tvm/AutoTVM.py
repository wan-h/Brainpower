# -*- coding: utf-8 -*-
# @Author  : wanhui

"""
https://tvm.apache.org/docs/tutorial/autotvm_relay_x86.html
Compiling and Optimizing a Model with the Python Interface (AutoTVM)
"""

import onnx
from PIL import Image
import numpy as np
import tvm
import tvm.relay as relay
from tvm.contrib import graph_executor
from tvm.contrib.download import download_testdata

"""
Downloading and Loading the ONNX Model
"""
print("=" * 50 + "Downloading and Loading the ONNX Model" + "=" * 50)
model_url = (
    "https://github.com/onnx/models/raw/main/"
    "vision/classification/resnet/model/"
    "resnet50-v2-7.onnx"
)

# 下载太慢了
# model_path = download_testdata(model_url, "resnet50-v2-7.onnx", module="onnx")
model_path = "resnet50-v2-7.onnx"
onnx_model = onnx.load(model_path)

"""
Downloading, Preprocessing, and Loading the Test Image
"""
print("=" * 50 + "Downloading, Preprocessing, and Loading the Test Image" + "=" * 50)
img_url = "https://s3.amazonaws.com/model-server/inputs/kitten.jpg"
# img_path = download_testdata(img_url, "kitten.jpg", module="data")
img_path = "kitten.jpg"
# resize
resized_image = Image.open(img_path).resize((224, 224))
img_data = np.asarray(resized_image).astype("float32")
# HWC -> CHW for onnx
img_data = np.transpose(img_data, (2, 0, 1))
# 输入归一化
imagenet_mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
imagenet_stddev = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
norm_img_data = (img_data / 255 - imagenet_mean) / imagenet_stddev
# 扩展batch维度
img_data = np.expand_dims(norm_img_data, axis=0)

"""
Compile the Model With Relay
"""
print("=" * 50 + "Compile the Model With Relay" + "=" * 50)
# 输入名称和维度可以使用netron查看
target = "llvm"
input_name = "data"
shape_dict = {input_name: img_data.shape}
# 前端获取模型
# mod是relay IR(本质上是一个OP占位符的function), params是参数字典
"""
# relay IR的表达式如下
# 函数的输入就是ONNX模型中所有输入Tensor的shape信息，不仅包含真实的输入input.1，还包含带权重OP的权重Tensor的shape信息，比如卷积层的weight和bias
# params字典中key就是tensor的名字，value就是TVM的Ndarry,存储真实的权重信息
def @main(%input.1: Tensor[(1, 3, 224, 224), float32], %v193: Tensor[(64, 3, 7, 7), float32], %v194: Tensor[(64), float32], %v196: Tensor[(64, 64, 3, 3), float32], %v197: Tensor[(64), float32], %v199: Tensor[(64, 64, 3, 3), float32], %v200: Tensor[(64), float32], %v202: Tensor[(64, 64, 3, 3), float32], %v203: Tensor[(64), float32], %v205: Tensor[(64, 64, 3, 3), float32], %v206: Tensor[(64), float32], %v208: Tensor[(128, 64, 3, 3), float32], %v209: Tensor[(128), float32], %v211: Tensor[(128, 128, 3, 3), float32], %v212: Tensor[(128), float32], %v214: Tensor[(128, 64, 1, 1), float32], %v215: Tensor[(128), float32], %v217: Tensor[(128, 128, 3, 3), float32], %v218: Tensor[(128), float32], %v220: Tensor[(128, 128, 3, 3), float32], %v221: Tensor[(128), float32], %v223: Tensor[(256, 128, 3, 3), float32], %v224: Tensor[(256), float32], %v226: Tensor[(256, 256, 3, 3), float32], %v227: Tensor[(256), float32], %v229: Tensor[(256, 128, 1, 1), float32], %v230: Tensor[(256), float32], %v232: Tensor[(256, 256, 3, 3), float32], %v233: Tensor[(256), float32], %v235: Tensor[(256, 256, 3, 3), float32], %v236: Tensor[(256), float32], %v238: Tensor[(512, 256, 3, 3), float32], %v239: Tensor[(512), float32], %v241: Tensor[(512, 512, 3, 3), float32], %v242: Tensor[(512), float32], %v244: Tensor[(512, 256, 1, 1), float32], %v245: Tensor[(512), float32], %v247: Tensor[(512, 512, 3, 3), float32], %v248: Tensor[(512), float32], %v250: Tensor[(512, 512, 3, 3), float32], %v251: Tensor[(512), float32], %fc.bias: Tensor[(1000), float32], %fc.weight: Tensor[(1000, 512), float32]) {
  %0 = nn.conv2d(%input.1, %v193, strides=[2, 2], padding=[3, 3, 3, 3], kernel_size=[7, 7]);
  %1 = nn.bias_add(%0, %v194);
  %2 = nn.relu(%1);
  %3 = nn.max_pool2d(%2, pool_size=[3, 3], strides=[2, 2], padding=[1, 1, 1, 1]);
  %4 = nn.conv2d(%3, %v196, padding=[1, 1, 1, 1], kernel_size=[3, 3]);
  %5 = nn.bias_add(%4, %v197);
  %6 = nn.relu(%5);
  ....
}
"""
mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

# PassContext定义了怎么去优化relay IR,例如算子融合等来优化计算图，从而提高模型推理效率
# OPT_PASS_LEVEL = {
#                 "SimplifyInference": 0,
#                 "OpFusion": 1,
#                 "FoldConstant": 2,
#                 "FoldScaleAxis": 3,
#                 "AlterOpLayout": 3,
#                 "CanonicalizeOps": 3,
#                 "CanonicalizeCast": 3,
#                 "EliminateCommonSubexpr": 3,
#                 "CombineParallelConv2D": 4,
#                 "CombineParallelDense": 4,
#                 "CombineParallelBatchMatmul": 4,
#                 "FastMath": 4
#             }

# 学习参考链接：https://mp.weixin.qq.com/s/CZzC5klWoFftUlOKkpvEZg
with tvm.transform.PassContext(opt_level=3):
    # mod是relay IR定义的图结构(main function)，params是权重，target是需要编译的目标硬件
    # build是将relay IR function编译成可执行程序的函数
    # 过程中才产生graph是优化后的更底层的图描述，优化图的权重，以及包含各种运行时库的tvm.Module
    # 输出lib就是将上面的IR，运行时库以及参数打包成一个tvm.Module，这样用户只需要把这个tvm.Module存下来，下次就可以省去编译过程直接在硬件上执行了
    lib = relay.build(mod, target=target, params=params)

# 获取tvm运行设备
dev = tvm.device(str(target), 0)
# relay.build的mod_name参数默认是default，所以这里通过default获取
module = graph_executor.GraphModule(lib["default"](dev))

"""
Execute on the TVM Runtime
"""
print("=" * 50 + "Execute on the TVM Runtime" + "=" * 50)
dtype = "float32"
module.set_input(input_name, img_data)
module.run()
output_shape = (1, 1000)
# tvm.nd就是tvm的ndarray
tvm_output = module.get_output(0, tvm.nd.empty(output_shape)).numpy()
"""
Collect Basic Performance Data
"""
print("=" * 50 + "Collect Basic Performance Data" + "=" * 50)
import timeit
timing_number = 10
timing_repeat = 10
# run module 耗时测试
# repeat参数是重复整个测试的次数，number参数是每个测试中调用被计时语句的次数
unoptimized = (
    np.array(timeit.Timer(lambda: module.run()).repeat(repeat=timing_repeat, number=timing_number))
    * 1000 / timing_number
)
unoptimized = {
    "mean": np.mean(unoptimized),
    "median": np.median(unoptimized),
    "std": np.std(unoptimized)
}
print(unoptimized)

"""
Postprocess the output
"""
print("=" * 50 + "Postprocess the output" + "=" * 50)
from scipy.special import softmax

# Download a list of labels
labels_url = "https://s3.amazonaws.com/onnx-model-zoo/synset.txt"
# labels_pth = download_testdata(labels_url, "synset.txt", module="data")
labels_pth = "synset.txt"
with open(labels_pth, "r") as f:
    labels = [l.rstrip() for l in f]

# Open the output and read the output tensor
scores = softmax(tvm_output)
scores = np.squeeze(scores)
ranks = np.argsort(scores)[::-1]
for rank in ranks[0: 5]:
    print("class='%s' with probability=%f" % (labels[rank], scores[rank]))

"""
Tune the model
"""
print("=" * 50 + "Tune the model" + "=" * 50)
import tvm.auto_scheduler as auto_scheduler
from tvm.autotvm.tuner import XGBTuner
from tvm import autotvm

number = 10
repeat = 1
min_repeat_ms = 0
timeout = 10
# create a TVM runner
runner = autotvm.LocalRunner(
    number=number,
    repeat=repeat,
    timeout=timeout,
    min_repeat_ms=min_repeat_ms,
    enable_cpu_cache_flush=True,
)
tuning_option = {
    "tuner": "xgb",
    "trials": 10,
    "early_stopping": 100,
    "measure_option": autotvm.measure_option(
        builder=autotvm.LocalBuilder(build_func="default"),
        runner=runner
    ),
    "tuning_records": "resnet-50-v2-autotuning.json",
}
# begin by extracting the tasks from the onnx model
tasks = autotvm.task.extract_from_program(mod["main"], target=target, params=params)
# Tune the extracted tasks sequentially.
for i, task in enumerate(tasks):
    prefix = "[Task %2d/%2d]" % (i + 1, len(tasks))
    tuner_obj = XGBTuner(task, loss_type="rank")
    tuner_obj.tune(
        n_trial=min(tuning_option["trials"], len(task.config_space)),
        early_stopping=tuning_option["early_stopping"],
        measure_option=tuning_option["measure_option"],
        callbacks=[
            autotvm.callback.progress_bar(tuning_option["trials"], prefix=prefix),
            autotvm.callback.log_to_file(tuning_option["tuning_records"])
        ],
    )

"""
Compiling an Optimized Model with Tuning Data
"""
print("=" * 50 + "Compiling an Optimized Model with Tuning Data" + "=" * 50)
with autotvm.apply_history_best(tuning_option["tuning_records"]):
    with tvm.transform.PassContext(opt_level=3, config={}):
        lib = relay.build(mod, target=target, params=params)
dev = tvm.device(str(target), 0)
module = graph_executor.GraphModule(lib["default"](dev))
# Verify that the optimized model runs and produces the same results:
dtype = "float32"
module.set_input(input_name, img_data)
module.run()
output_shape = (1, 1000)
tvm_output = module.get_output(0, tvm.nd.empty(output_shape)).numpy()

scores = softmax(tvm_output)
scores = np.squeeze(scores)
ranks = np.argsort(scores)[::-1]
for rank in ranks[0:5]:
    print("class='%s' with probability=%f" % (labels[rank], scores[rank]))

"""
Comparing the Tuned and Untuned Models
"""
print("=" * 50 + "Comparing the Tuned and Untuned Models" + "=" * 50)
import timeit

timing_number = 10
timing_repeat = 10
optimized = (
    np.array(timeit.Timer(lambda: module.run()).repeat(repeat=timing_repeat, number=timing_number))
    * 1000 / timing_number
)
optimized = {"mean": np.mean(optimized), "median": np.median(optimized), "std": np.std(optimized)}


print("optimized: %s" % (optimized))
print("unoptimized: %s" % (unoptimized))