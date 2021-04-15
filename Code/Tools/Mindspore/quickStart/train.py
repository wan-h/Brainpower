# coding: utf-8
# Author: wanhui0729@gmail.com

'''
下载数据集
!mkdir -p ./datasets/cifar10/train ./datasets/cifar10/test
wget http://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz 然后分train test
'''

import os, sys
import time
import numpy as np
import mindspore
from mindspore import context
import mindspore.nn as nn
from mindspore.train.callback import Callback
from mindspore.nn import SoftmaxCrossEntropyWithLogits
from mindspore import Tensor, Model
from mindspore.train.callback import ModelCheckpoint, CheckpointConfig, LossMonitor
from mindspore.nn import Accuracy
from mindspore import load_checkpoint, load_param_into_net
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from resnet import resnet18, resnet50, resnet101
from dataset import create_dataset

# 配置运行信息
context.set_context(mode=context.GRAPH_MODE, device_target='Ascend')


# 自定义回调函数收集模型的损失值和精度值
# 该类继承了Callback类，可以自定义训练过程中的操作，等训练完成后，可将数据绘成图查看step与loss的变化情况，以及step与accuracy的变化情况。
class StepLossAccInfo(Callback):
    def __init__(self, model, eval_dataset, steps_loss, steps_eval):
        self.model = model
        self.eval_dataset = eval_dataset
        self.steps_loss = steps_loss
        self.steps_eval = steps_eval

    def step_end(self, run_context):
        cb_params = run_context.original_args()
        cur_epoch = cb_params.cur_epoch_num
        cur_step = (cur_epoch-1)*1875 + cb_params.cur_step_num
        self.steps_loss["loss_value"].append(str(cb_params.net_outputs))
        self.steps_loss["step"].append(str(cur_step))
        if cur_step % 125 == 0:
            acc = self.model.eval(self.eval_dataset, dataset_sink_mode=False)
            self.steps_eval["step"].append(cur_step)
            self.steps_eval["acc"].append(acc["Accuracy"])

# 定义损失函数及优化器
# create the network
network = resnet101()
# define the optimizer
net_opt = nn.Momentum(network.trainable_params(), learning_rate=0.01, momentum=0.9)
# define the loss function
net_loss = SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')

# 训练网络
epoch_size = 10
data_path = "./datasets/cifar10"
model_path = "./models/ckpt/"

repeat_size = 1
ds_train = create_dataset(os.path.join(data_path, "train"), 32, repeat_size)
eval_dataset = create_dataset(os.path.join(data_path, "test"), 32)

# clean up old run files before in Linux
os.system('rm -f {0}*.ckpt {0}*.meta {0}*.pb'.format(model_path))

# define the model
model = Model(network, net_loss, net_opt, metrics={"Accuracy": Accuracy()} )

# save the network model and parameters for subsequence fine-tuning
config_ck = CheckpointConfig(save_checkpoint_steps=100, keep_checkpoint_max=20)
# group layers into an object with training and evaluation features
ckpoint_cb = ModelCheckpoint(prefix="checkpoint_resnet18", directory=model_path, config=config_ck)

steps_loss = {"step": [], "loss_value": []}
steps_eval = {"step": [], "acc": []}
# collect the steps,loss and accuracy information
step_loss_acc_info = StepLossAccInfo(model, eval_dataset, steps_loss, steps_eval)

# print("================ Start training ================")
# model.train(epoch_size, ds_train, callbacks=[ckpoint_cb, LossMonitor(20), step_loss_acc_info], dataset_sink_mode=False)


# print("================ transfer learning ================")
# param_dict = load_checkpoint("./models/ckpt/mindspore_quick_start/checkpoint_lenet-1_1875.ckpt")
# network = resnet18()
# opt = nn.Momentum(network.trainable_params(), learning_rate=0.01, momentum=0.9)
# ds_train = create_dataset(os.path.join(data_path, "train"), 32, repeat_size)
# # load parameter to the network
# load_param_into_net(network, param_dict)
# # load the parameter into optimizer
# load_param_into_net(opt, param_dict)
# loss = SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')
# model = Model(network, loss, opt)
# model.train(1, ds_train, callbacks=[ckpoint_cb, LossMonitor(125), step_loss_acc_info], dataset_sink_mode=False)

# 验证模型
def test_net(network, model, data_path):
    """Define the evaluation method."""
    print("============== Starting Testing ==============")
    # load the saved model for evaluation
    checkpoint = "./101.ckpt"
    _t = time.time()
    param_dict = load_checkpoint(checkpoint)
    # load parameter to the network
    load_param_into_net(network, param_dict)
    print(f"Load params to model cost: {time.time() - _t} s")

    # inference
    print("============== Infer Testing ==============")
    input_data = Tensor(np.random.randint(0, 255, [1, 3, 224, 224]), mindspore.float32)

    infer_time = 0
    while infer_time < 21:
        _t = time.time()
        model.predict(input_data)
        print(f"Model infer cost: {time.time() - _t} s")
        infer_time += 1

    # load testing dataset
    # ds_eval = create_dataset(os.path.join(data_path, "test"))
    # acc = model.eval(ds_eval, dataset_sink_mode=False)
    # print("============== Accuracy:{} ==============".format(acc))

test_net(network, model, data_path)