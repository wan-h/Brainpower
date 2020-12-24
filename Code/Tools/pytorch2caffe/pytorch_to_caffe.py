# coding: utf-8
# Author: wanhui0729@gmail.com

import traceback
import torch
import re
from rock.dl import layers
from functools import reduce
import numpy as np
from math import ceil
from torch import Tensor as t
import torch.nn.functional as F
from torch.nn.modules.utils import _pair
from .Caffe import caffe_net
from .transLog import TransLog

"""
How to support a new layer type:
 layer_name=log.add_layer(layer_type_name)
 top_blobs=log.add_blobs(<output of that layer>)
 layer=caffe_net.Layer_param(xxx)
 <set layer parameters>
 [<layer.add_data(*datas)>]
 log.cnet.add_layer(layer)

Please try MUTE the inplace operations to avoid not find in graph
"""

NET_INITTED = False
#
VIEW2FLATTEN = False
FLATTEN2VIEW = False
RELU6TORELU = False
log = TransLog()
layer_names = {}


def _conv2d(raw, input, weight, bias=None, stride=1, padding=0, dilation=1, groups=1):
    x = raw(input, weight, bias, stride, padding, dilation, groups)
    name = log.add_layer(name='conv')
    log.add_blobs([x], name='conv_blob')
    layer = caffe_net.Layer_param(name=name, type='Convolution', bottom=[log.blobs(input)], top=[log.blobs(x)])
    layer.conv_param(x.size()[1], weight.size()[2:], stride=_pair(stride),
                     pad=_pair(padding), dilation=_pair(dilation), bias_term=bias is not None, groups=groups)
    if bias is not None:
        layer.add_data(weight.cpu().data.numpy(), bias.cpu().data.numpy())
    else:
        layer.param.convolution_param.bias_term = False
        layer.add_data(weight.cpu().data.numpy())
    log.cnet.add_layer(layer)
    return x

def _conv_transpose2d(raw, input, weight, bias=None, stride=1, padding=0, output_padding=0, groups=1, dilation=1):
    x = raw(input, weight, bias, stride, padding, output_padding, groups, dilation)
    name = log.add_layer(name='conv_transpose')
    log.add_blobs([x], name='conv_transpose_blob')
    layer = caffe_net.Layer_param(name=name, type='Deconvolution', bottom=[log.blobs(input)], top=[log.blobs(x)])
    layer.conv_param(x.size()[1], weight.size()[2:], stride=_pair(stride),
                     pad=_pair(padding), dilation=_pair(dilation), bias_term=bias is not None)
    if bias is not None:
        layer.add_data(weight.cpu().data.numpy(), bias.cpu().data.numpy())
    else:
        layer.param.convolution_param.bias_term=False
        layer.add_data(weight.cpu().data.numpy())
    log.cnet.add_layer(layer)
    return x

def _linear(raw, input, weight, bias=None):
    x = raw(input, weight, bias)
    layer_name = log.add_layer(name='fc')
    top_blobs = log.add_blobs([x], name='fc_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='InnerProduct', bottom=[log.blobs(input)], top=top_blobs)
    layer.fc_param(x.size()[1], has_bias=bias is not None)
    if bias is not None:
        layer.add_data(weight.cpu().data.numpy(), bias.cpu().data.numpy())
    else:
        layer.add_data(weight.cpu().data.numpy())
    log.cnet.add_layer(layer)
    return x

def _split(raw, tensor, split_size, dim=0):
    # split in pytorch is slice in caffe
    x = raw(tensor, split_size, dim)
    layer_name = log.add_layer('split')
    top_blobs = log.add_blobs(x, name='split_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Slice', bottom=[log.blobs(tensor)], top=top_blobs)
    slice_num = int(np.floor(tensor.size()[dim]/split_size))
    slice_param = caffe_net.pb.SliceParameter(axis=dim, slice_point=[split_size*i for i in range(1, slice_num)])
    layer.param.slice_param.CopyFrom(slice_param)
    log.cnet.add_layer(layer)
    return x

def _pool(pool_type, raw, input, x, kernel_size, stride, padding, ceil_mode):
    layer_name = log.add_layer(name='{}_pool'.format(pool_type))
    top_blobs = log.add_blobs([x], name='{}_pool_blob'.format(pool_type))
    layer = caffe_net.Layer_param(name=layer_name, type='Pooling', bottom=[log.blobs(input)], top=top_blobs)
    in_b, in_c, in_h, in_w = input.size()
    if _pair(kernel_size)[0] == in_h and _pair(kernel_size)[1] == in_w:
        layer.pool_param(type=pool_type.upper(), global_pooling=True)
        log.cnet.add_layer(layer)
        return
    # processing dilation
    # pytorch，默认dilation=1，caffe参数暂不支持，处理时直接忽略dilation的影响

    # processing ceil mode
    # in_b, in_c, in_h, in_w = input.size()
    # if type(kernel_size) == int and kernel_size == in_h == in_w:
    #     layer.pool_param(type=pool_type.upper(), global_pooling=True)
    # else:
    #     layer.pool_param(kernel_size=kernel_size, stride=kernel_size if stride is None else stride,
        # 				 pad=padding, type=pool_type.upper())
    # log.cnet.add_layer(layer)
    # if ceil_mode == False and stride is not None:
    #     oheight = (input.size()[2] - _pair(kernel_size)[0] + 2 * _pair(padding)[0]) % (_pair(stride)[0])
    #     owidth = (input.size()[3] - _pair(kernel_size)[1] + 2 * _pair(padding)[1]) % (_pair(stride)[1])
    #     if oheight != 0 or owidth != 0:
    #         caffe_out = raw(input, kernel_size, stride, padding, ceil_mode=True)
    #         print("WARNING: the output shape miss match at {}: input {} output---Pytorch:{}---Caffe:{}\n"
    #               "This is caused by the different implementation that ceil mode in caffe and the floor mode in pytorch.\n"
    #               "You can add the clip layer in caffe prototxt manually if shape mismatch error is caused in caffe. "
    #               .format(layer_name, input.size(), x.size(), caffe_out.size()))

    # processing ceil mode
    # caffe默认使用ceil mode为false,pytorch默认为true,若两种实现存在偏差，则通过解析修正caffe中的偏差
    oheight = (input.size()[2] - _pair(kernel_size)[0] + 2 * _pair(padding)[0]) % (_pair(stride)[0])
    owidth = (input.size()[3] - _pair(kernel_size)[1] + 2 * _pair(padding)[1]) % (_pair(stride)[1])
    if ceil_mode == False and (oheight != 0 or owidth != 0):
        caffe_out = raw(input, kernel_size, stride, padding, ceil_mode=True)
        print("WARNING: the output shape miss match at {}: input {} output---Pytorch:{}---Caffe:{}\n"
              "This is caused by the different implementation that ceil mode in caffe and the floor mode in pytorch.\n"
              "You can add the clip layer in caffe prototxt manually if shape mismatch error is caused in caffe.\n"
              "Tool try fine tune this problem. "
              .format(layer_name, input.size(), x.size(), caffe_out.size()))
        pytorch_out_h, pytorch_out_w = x.size()[-2:]
        new_padding_h = int(_pair(padding)[0])
        new_padding_w = int(_pair(padding)[1])
        new_kernel_h = int(_pair(kernel_size)[0])
        new_kernel_w = int(_pair(kernel_size)[1])
        padding_h_fine_tune_ok = False
        padding_w_fine_tune_ok = False
        kernel_h_fine_tune_ok = False
        kernel_w_fine_tune_ok = False
        # 通过padding修正
        if padding is not None:
            while new_padding_h > 0:
                new_padding_h -= 1
                if ceil((input.size()[2] - _pair(kernel_size)[0] + 2 * new_padding_h) / (_pair(stride)[0])) \
                        == pytorch_out_h - 1:
                    padding_h_fine_tune_ok = True
                    kernel_h_fine_tune_ok = True
                    break
            while new_padding_w > 0:
                new_padding_w -= 1
                if ceil((input.size()[3] - _pair(kernel_size)[1] + 2 * new_padding_w) / (_pair(stride)[1])) \
                        == pytorch_out_w - 1:
                    padding_w_fine_tune_ok = True
                    kernel_w_fine_tune_ok = True
                    break
        new_padding = (new_padding_h, new_padding_w)

        # 通过kernel修正
        if not padding_h_fine_tune_ok:
            while new_kernel_h > 0:
                new_kernel_h -= 1
                if ceil((input.size()[2] - new_kernel_h) / (_pair(stride)[0])) == pytorch_out_h - 1:
                    kernel_h_fine_tune_ok = True
                    break
        if not padding_w_fine_tune_ok:
            while new_kernel_w > 0:
                new_kernel_w -= 1
                if ceil((input.size()[3] - new_kernel_w) / (_pair(stride)[1])) == pytorch_out_w - 1:
                    kernel_w_fine_tune_ok = True
                    break
        new_kernel_size = (new_kernel_h, new_kernel_w)
        # 当前只支持上下左右padding相同的模式
        if kernel_h_fine_tune_ok and kernel_w_fine_tune_ok and new_padding[0] == new_padding[1]:
            print("And fine tune successfully !")
            layer.pool_param(kernel_size=new_kernel_size, stride=kernel_size if stride is None else stride,
                             pad=new_padding[0], type=pool_type.upper())
            log.cnet.add_layer(layer)
            return
        else:
            print("But fine tune failed !")

    layer.pool_param(kernel_size=kernel_size, stride=kernel_size if stride is None else stride,
                         pad=padding, type=pool_type.upper())
    log.cnet.add_layer(layer)

def _max_pool2d(raw, input, kernel_size, stride=None, padding=0, dilation=1, ceil_mode=False, return_indices=False):
    x = raw(input, kernel_size, stride, padding, dilation, ceil_mode, return_indices)
    _pool('max', raw, input, x, kernel_size, stride, padding, ceil_mode)
    return x

def _avg_pool2d(raw, input, kernel_size, stride = None, padding = 0, ceil_mode = False, count_include_pad = True,
                divisor_override=None):
    x = raw(input, kernel_size, stride, padding, ceil_mode, count_include_pad, divisor_override)
    _pool('ave', raw, input, x, kernel_size, stride, padding, ceil_mode)
    return x

# 通过kernel, stride将adaptive_pool强制调整为普通pool
def _parse_adaptive_pool_param(input, output_size):
    print("WARNING: adaptive_pool operation is special for caffe."
          "Tool try fine tune this problem. ")
    output_size_h = _pair(output_size)[0]
    output_size_w = _pair(output_size)[1]
    in_b, in_c, in_h, in_w = input.size()

    # 不支持尺度小于2的pool操作，强制补padding会带来较大误差
    assert (in_h >= output_size_h * 2 - 1) or (in_w >= output_size_w * 2 - 1), \
        "Pytorch2caffe not support adaptive_pool input size < 2 * output_size - 1"
    kernel_h = ceil(in_h / output_size_h)
    kernel_w = ceil(in_w / output_size_w)
    stride = kernel_size = (kernel_h, kernel_w)
    print("And fine tune successfully !")
    return kernel_size, stride

def _adaptive_avg_pool2d(raw, input, output_size):
    kernel_size, stride = _parse_adaptive_pool_param(input, output_size)
    x = raw(input, output_size)
    _pool('ave', F.avg_pool2d, input, x, kernel_size, stride, padding=0, ceil_mode=True)
    return x

def _adaptive_max_pool2d(raw, input, output_size):
    kernel_size, stride = _parse_adaptive_pool_param(input, output_size)
    x = raw(input, output_size)
    _pool('max', F.max_pool2d, input, x, kernel_size, stride, padding=0, ceil_mode=True)
    return x

def _max(raw, *args):
    x = raw(*args)
    if len(args)==1:
        # TODO max in one tensor
        assert NotImplementedError
    else:
        bottom_blobs = []
        for arg in args:
            bottom_blobs.append(log.blobs(arg))
        layer_name = log.add_layer(name='max')
        top_blobs = log.add_blobs([x], name='max_blob')
        layer = caffe_net.Layer_param(name=layer_name, type='Eltwise', bottom=bottom_blobs, top=top_blobs)
        layer.param.eltwise_param.operation = 2
        log.cnet.add_layer(layer)
    return x

def _cat(raw, inputs, dim=0):
    x = raw(inputs, dim)
    bottom_blobs = []
    for input in inputs:
        bottom_blobs.append(log.blobs(input))
    layer_name = log.add_layer(name='cat')
    top_blobs = log.add_blobs([x], name='cat_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Concat', bottom=bottom_blobs, top=top_blobs)
    layer.param.concat_param.axis = dim
    log.cnet.add_layer(layer)
    return x

def _dropout(raw, input, p=0.5, training=False, inplace=False):
    x = raw(input, p, training, inplace)
    bottom_blobs = [log.blobs(input)]
    layer_name = log.add_layer(name='dropout')
    top_blobs = log.add_blobs([x], name=bottom_blobs[0], with_num=False)
    layer = caffe_net.Layer_param(name=layer_name, type='Dropout', bottom=bottom_blobs, top=top_blobs)
    layer.param.dropout_param.dropout_ratio = p
    layer.param.include.extend([caffe_net.pb.NetStateRule(phase=0)]) # 1 for test, 0 for train
    log.cnet.add_layer(layer)
    return x

def _threshold(raw, input, threshold, value, inplace=False):
    # for threshold or relu
    if threshold == 0 and value == 0:
        x = raw(input, threshold, value, inplace)
        bottom_blobs = [log.blobs(input)]
        name = log.add_layer(name='relu')
        log.add_blobs([x], name='relu_blob')
        layer = caffe_net.Layer_param(name=name, type='ReLU', bottom=bottom_blobs, top=[log.blobs(x)])
        log.cnet.add_layer(layer)
        return x
    if value != 0:
        raise NotImplemented("value !=0 not implemented in caffe")
    x = raw(input, input, threshold, value, inplace)
    bottom_blobs = [log.blobs(input)]
    layer_name = log.add_layer(name='threshold')
    top_blobs = log.add_blobs([x], name='threshold_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Threshold', bottom=bottom_blobs, top=top_blobs)
    layer.param.threshold_param.threshold = threshold
    log.cnet.add_layer(layer)
    return x

def _relu(raw, input, inplace=False):
    # for threshold or prelu
    x = raw(input, inplace=False)
    name = log.add_layer(name='relu')
    log.add_blobs([x], name='relu_blob')
    layer = caffe_net.Layer_param(name=name, type='ReLU', bottom=[log.blobs(input)], top=[log.blobs(x)])
    log.cnet.add_layer(layer)
    return x

# only support relu6
def _hardtanh(raw, input, min_val=-1., max_val=1.,inplace=False):
    assert RELU6TORELU, "only support relu6, please check parameter relu6torelu=True"
    assert min_val == 0. and max_val == 6., "Only support relu6, min_val=0., max_val=6."
    x = raw(input, min_val=min_val, max_val=min_val, inplace=False)
    # 调用relu
    name = log.add_layer(name='relu')
    log.add_blobs([x], name='relu_blob')
    layer = caffe_net.Layer_param(name=name, type='ReLU', bottom=[log.blobs(input)], top=[log.blobs(x)])
    log.cnet.add_layer(layer)
    return x


def _sigmoid(raw, input):
    # for threshold or prelu
    x = raw(input)
    name = log.add_layer(name='sigmoid')
    log.add_blobs([x], name='sigmoid_blob')
    layer = caffe_net.Layer_param(name=name, type='Sigmoid', bottom=[log.blobs(input)], top=[log.blobs(x)])
    log.cnet.add_layer(layer)
    return x

def _prelu(raw, input, weight):
    # for threshold or prelu
    x = raw(input, weight)
    bottom_blobs = [log.blobs(input)]
    name = log.add_layer(name='prelu')
    log.add_blobs([x], name='prelu_blob')
    layer = caffe_net.Layer_param(name=name, type='PReLU', bottom=bottom_blobs, top=[log.blobs(x)])
    if weight.size()[0] == 1:
        layer.param.prelu_param.channel_shared=True
        layer.add_data(weight.cpu().data.numpy()[0])
    else:
        layer.add_data(weight.cpu().data.numpy())
    log.cnet.add_layer(layer)
    return x

def _leaky_relu(raw, input, negative_slope=0.01, inplace=False):
    x = raw(input, negative_slope)
    name = log.add_layer(name='leaky_relu')
    log.add_blobs([x], name='leaky_relu_blob')
    layer = caffe_net.Layer_param(name=name, type='ReLU', bottom=[log.blobs(input)], top=[log.blobs(x)])
    layer.param.relu_param.negative_slope = negative_slope
    log.cnet.add_layer(layer)
    return x

def _tanh(raw, input):
    # for tanh activation
    x = raw(input)
    name = log.add_layer(name='tanh')
    log.add_blobs([x], name='tanh_blob')
    layer = caffe_net.Layer_param(name=name, type='TanH', bottom=[log.blobs(input)], top=[log.blobs(x)])
    log.cnet.add_layer(layer)
    return x

def _softmax(raw, input, dim=None, _stacklevel=3):
    # for F.softmax
    x = raw(input, dim=dim)
    if dim is None:
        dim = F._get_softmax_dim('softmax', input.dim(), _stacklevel)
    elif dim == -1:
        dim = input.dim() - 1
    bottom_blobs = [log.blobs(input)]
    name = log.add_layer(name='softmax')
    log.add_blobs([x], name='softmax_blob')
    layer = caffe_net.Layer_param(name=name, type='Softmax', bottom=bottom_blobs, top=[log.blobs(x)])
    layer.param.softmax_param.axis = dim
    log.cnet.add_layer(layer)
    return x

def _batch_norm(raw, input, running_mean, running_var, weight=None, bias=None,
                training=False, momentum=0.1, eps=1e-5):
    # because the runing_mean and runing_var will be changed after the _batch_norm operation, we first save the parameters
    x = raw(input, running_mean, running_var, weight, bias,
            training, momentum, eps)
    bottom_blobs = [log.blobs(input)]
    layer_name1 = log.add_layer(name='batch_norm')
    top_blobs = log.add_blobs([x], name='batch_norm_blob')
    layer1 = caffe_net.Layer_param(name=layer_name1, type='BatchNorm', bottom=bottom_blobs, top=top_blobs)
    if running_mean is None or running_var is None:
        # not use global_stats, normalization is performed over the current mini-batch
        layer1.batch_norm_param(use_global_stats=0, eps=eps)
    else:
        layer1.batch_norm_param(use_global_stats=1, eps=eps)
        running_mean_clone = running_mean.clone()
        running_var_clone = running_var.clone()
        layer1.add_data(running_mean_clone.cpu().numpy(), running_var_clone.cpu().numpy(), np.array([1.0]))
    log.cnet.add_layer(layer1)
    if weight is not None and bias is not None:
        layer_name2 = log.add_layer(name='bn_scale')
        layer2 = caffe_net.Layer_param(name=layer_name2, type='Scale', bottom=top_blobs, top=top_blobs)
        layer2.param.scale_param.bias_term = True
        layer2.add_data(weight.cpu().data.numpy(), bias.cpu().data.numpy())
        log.cnet.add_layer(layer2)
    return x

def _instance_norm(raw, input, running_mean=None, running_var=None, weight=None,
                   bias=None, use_input_stats=True, momentum=0.1, eps=1e-5):
    # TODO: the batch size!=1 view operations
    print("WARNING: The Instance Normalization transfers to Caffe using BatchNorm, so the batch size should be 1")
    if running_var is not None or weight is not None:
        # TODO: the affine=True or track_running_stats=True case
        raise NotImplementedError("not implement the affine=True or track_running_stats=True case InstanceNorm")
    x = torch.batch_norm(
        input, weight, bias, running_mean, running_var,
        use_input_stats, momentum, eps, torch.backends.cudnn.enabled)
    bottom_blobs = [log.blobs(input)]
    layer_name1 = log.add_layer(name='instance_norm')
    top_blobs = log.add_blobs([x], name='instance_norm_blob')
    layer1 = caffe_net.Layer_param(name=layer_name1, type='BatchNorm',
                                   bottom=bottom_blobs, top=top_blobs)
    if running_mean is None or running_var is None:
        # not use global_stats, normalization is performed over the current mini-batch
        layer1.batch_norm_param(use_global_stats=0,eps=eps)
        running_mean=torch.zeros(input.size()[1])
        running_var=torch.ones(input.size()[1])
    else:
        layer1.batch_norm_param(use_global_stats=1, eps=eps)
    running_mean_clone = running_mean.clone()
    running_var_clone = running_var.clone()
    layer1.add_data(running_mean_clone.cpu().numpy(), running_var_clone.cpu().numpy(), np.array([1.0]))
    log.cnet.add_layer(layer1)
    if weight is not None and bias is not None:
        layer_name2 = log.add_layer(name='bn_scale')
        layer2 = caffe_net.Layer_param(name=layer_name2, type='Scale',
                                       bottom=top_blobs, top=top_blobs)
        layer2.param.scale_param.bias_term = True
        layer2.add_data(weight.cpu().data.numpy(), bias.cpu().data.numpy())
        log.cnet.add_layer(layer2)
    return x

#upsample layer
def _upsample(raw, input, size=None, scale_factor=None, mode='nearest', align_corners=None):
    # 定义的参数包括 scale,即输出与输入的尺寸比例,如 2;scale_h、scale_w,
    # 同 scale,分别为 h、w 方向上的尺寸比例;pad_out_h、pad_out_w,仅在 scale 为 2 时
    # 有用,对输出进行额外 padding 在 h、w 方向上的数值;upsample_h、upsample_w,输
    # 出图像尺寸的数值。在 Upsample 的相关代码中,推荐仅仅使用 upsample_h、
    # upsample_w 准确定义 Upsample 层的输出尺寸,其他所有的参数都不推荐继续使用。
    # for nearest _interpolate
    if mode != "nearest" or align_corners != None:
        raise NotImplementedError("not implement F.interpolate totoaly")
    x = raw(input, size, scale_factor, mode)

    layer_name = log.add_layer(name='upsample')
    top_blobs = log.add_blobs([x], name='upsample_blob'.format(type))
    layer = caffe_net.Layer_param(name=layer_name, type='Upsample', bottom=[log.blobs(input)], top=top_blobs)
    layer.upsample_param(size=(input.size(2), input.size(3)), scale_factor=scale_factor)
    log.cnet.add_layer(layer)
    return x


def _interpolate(raw, input, size=None, scale_factor=None, mode='bilinear', align_corners=None):
    if mode != "bilinear":
        raise NotImplementedError("only implement F.interpolate bilinear mode.")
    x = raw(input, size, scale_factor, mode, align_corners)

    layer_name = log.add_layer(name='interp')
    top_blobs = log.add_blobs([x], name='interp_blob'.format(type))
    layer = caffe_net.Layer_param(name=layer_name, type='Interp',
                                  bottom=[log.blobs(input)], top=top_blobs)
    if size:
        layer.interp_param(size=size)
    elif scale_factor:
        layer.interp_param(size=(input.size(2) * scale_factor, input.size(3) * scale_factor))
    else:
        raise Exception("F.interpolate must has size or scale_factor param.")

    log.cnet.add_layer(layer)
    return x


def _l2norm(raw, input, weight, gamma, eps):
    x = raw(input, weight, gamma, eps)
    bottom_blobs = [log.blobs(input)]
    layer_name = log.add_layer(name='normlize')
    top_blobs = log.add_blobs([x], name='normlize_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Normalize', bottom=bottom_blobs, top=top_blobs)
    layer.param.norm_param.across_spatial = False
    layer.param.norm_param.scale_filler.type = "constant"
    layer.param.norm_param.scale_filler.value = gamma
    layer.param.norm_param.channel_shared = False
    layer.add_data(weight.cpu().data.numpy())
    log.cnet.add_layer(layer)
    return x


def _permute(input, *args):
    x = raw_permute(input, *args)
    bottom_blobs = [log.blobs(input)]
    layer_name = log.add_layer(name='permute')
    top_blobs = log.add_blobs([x], name='permute_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Permute', bottom=bottom_blobs, top=top_blobs)
    layer.param.permute_param.order.extend(args)
    log.cnet.add_layer(layer)
    return x

def _contiguous(input, *args):
    x = raw_contiguous(input, *args)
    if not NET_INITTED:
        return x
    blob_id = int(id(x))
    pre_blob_val = log.blobs(input)
    log._blobs[blob_id] = pre_blob_val
    # top_blobs=log.add_blobs([x],name='contiguous_blob')
    return x

def _flatten(input, *args):
    if FLATTEN2VIEW:
        args_list = list(args)
        # 直接展平
        input_shape = input.shape
        start_dim, end_dim = 0, len(input_shape) - 1
        if len(args_list) == 0:
            return _view(input, 1, -1)
        elif len(args_list) == 1:
            start_dim = args_list[0]
        elif len(args_list) == 2:
            start_dim = args_list[0]
            end_dim = args_list[1]
        view_args_list = []
        flatten_size = 1
        for index, shape in enumerate(input_shape):
            if index >= start_dim and index <= end_dim:
                flatten_size *= shape
                if index == end_dim:
                    view_args_list.append(flatten_size)
                    flatten_size = 1
            else:
                view_args_list.append(shape)
        return _view(input, *view_args_list)
    x = raw_faltten(input, *args)
    bottom_blobs = [log.blobs(input)]
    layer_name = log.add_layer(name='flatten')
    top_blobs = log.add_blobs([x], name='flatten_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Flatten', bottom=bottom_blobs, top=top_blobs)
    layer.flatten_param(*args)
    log.cnet.add_layer(layer)
    return x

def _view(input, *args):
    x = raw_view(input, *args)
    if not NET_INITTED:
        return x
    input_shape = input.shape
    args_list = list(args)
    # 适配起始位置为0的写法
    if args_list[0] == -1:
        args_list[0] = reduce(lambda x, y: x*y, input_shape) // reduce(lambda x, y: x*y, args_list[1:])
    assert input_shape[0] == args_list[0], "View operation's first dim should be batch_size"
    if VIEW2FLATTEN and -1 in args_list:
        for index, input_shape_dim in enumerate(input_shape):
            if args_list[index] == -1:
                # 找到起始维度
                start_dim = index
                if index + 1 == len(args_list):
                    return _flatten(input, start_dim)
                else:
                    end_args = args_list[index+1:]
                    if end_args == input_shape[-len(end_args):]:
                        end_dim = len(input_shape) - len(end_args) - 1
                        return _flatten(input, start_dim, end_dim)
                break
            else:
                if input_shape_dim != args_list[index]:
                    break
        print("WARNING: Try transform from view operation to flatten operation failed.")
    layer_name = log.add_layer(name='view')
    top_blobs = log.add_blobs([x], name='view_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Reshape', bottom=[log.blobs(input)], top=top_blobs)

    dims = list(args)
    # if first dim is batch_size, should be set 0.
    if args_list[0] == input_shape[0]:
        dims[0] = 0

    layer.param.reshape_param.shape.CopyFrom(caffe_net.pb.BlobShape(dim=dims))
    # layer.param.reshape_param.shape.dim.extend(dims)
    log.cnet.add_layer(layer)
    return x

def _reshape(input, *args):
    x = raw_reshape(input, *args)
    if not NET_INITTED:
        return x
    input_shape = input.shape
    args_list = list(args)
    layer_name = log.add_layer(name='reshape')
    top_blobs = log.add_blobs([x], name='reshape_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Reshape', bottom=[log.blobs(input)], top=top_blobs)

    dims = list(args)
    # if first dim is batch_size, should be set 0.
    if args_list[0] == input_shape[0]:
        dims[0] = 0

    layer.param.reshape_param.shape.CopyFrom(caffe_net.pb.BlobShape(dim=dims))
    # layer.param.reshape_param.shape.dim.extend(dims)
    log.cnet.add_layer(layer)
    return x

def _mean(input, *args,**kwargs):
    x = raw_mean(input, *args, **kwargs)
    if not NET_INITTED:
        return x
    layer_name = log.add_layer(name='mean')
    top_blobs = log.add_blobs([x], name='mean_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Reduction', bottom=[log.blobs(input)], top=top_blobs)
    if len(args) == 1:
        dim = args[0]
    elif 'dim' in kwargs:
        dim = kwargs['dim']
    else:
        raise NotImplementedError('mean operation must specify a dim')
    layer.param.reduction_param.operation = 4
    layer.param.reduction_param.axis = dim
    log.cnet.add_layer(layer)
    return x

def _add(input, *args):
    x = raw__add__(input, *args)
    if not NET_INITTED:
        return x
    layer_name = log.add_layer(name='add')
    top_blobs = log.add_blobs([x], name='add_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Eltwise', bottom=[log.blobs(input), log.blobs(args[0])], top=top_blobs)
    layer.param.eltwise_param.operation = 1 # sum is 1
    log.cnet.add_layer(layer)
    return x

def _iadd(input, *args):
    x = raw__iadd__(input, *args)
    if not NET_INITTED:
        return x
    x = x.clone()
    layer_name = log.add_layer(name='add')
    top_blobs = log.add_blobs([x], name='add_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Eltwise', bottom=[log.blobs(input), log.blobs(args[0])], top=top_blobs)
    layer.param.eltwise_param.operation = 1 # sum is 1
    log.cnet.add_layer(layer)
    return x

def _sub(input, *args):
    x = raw__sub__(input, *args)
    if not NET_INITTED:
        return x
    layer_name = log.add_layer(name='sub')
    top_blobs = log.add_blobs([x], name='sub_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Eltwise', bottom=[log.blobs(input), log.blobs(args[0])], top=top_blobs)
    layer.param.eltwise_param.operation = 1 # sum is 1
    layer.param.eltwise_param.coeff.extend([1., -1.])
    log.cnet.add_layer(layer)
    return x

def _isub(input, *args):
    x = raw_isub__(input, *args)
    if not NET_INITTED:
        return x
    x = x.clone()
    layer_name = log.add_layer(name='sub')
    top_blobs = log.add_blobs([x], name='sub_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Eltwise', bottom=[log.blobs(input), log.blobs(args[0])], top=top_blobs)
    layer.param.eltwise_param.operation = 1 # sum is 1
    log.cnet.add_layer(layer)
    return x

def _mul(input, *args):
    x = raw__mul__(input, *args)
    if not NET_INITTED:
        return x
    layer_name = log.add_layer(name='mul')
    top_blobs = log.add_blobs([x], name='mul_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Eltwise', bottom=[log.blobs(input), log.blobs(args[0])], top=top_blobs)
    layer.param.eltwise_param.operation = 0  # product is 1
    log.cnet.add_layer(layer)
    return x

def _imul(input, *args):
    x = raw__imul__(input, *args)
    if not NET_INITTED:
        return x
    x = x.clone()
    layer_name = log.add_layer(name='mul')
    top_blobs = log.add_blobs([x], name='mul_blob')
    layer = caffe_net.Layer_param(name=layer_name, type='Eltwise', bottom=[log.blobs(input), log.blobs(args[0])], top=top_blobs)
    layer.param.eltwise_param.operation = 0  # product is 1
    layer.param.eltwise_param.coeff.extend([1., -1.])
    log.cnet.add_layer(layer)
    return x


# 核心组件，实现对torch的function中的operators的输入，输出以及参数的读取
class Rp(object):
    def __init__(self, raw, replace, **kwargs):
        # replace the raw function to replace function
        self.obj = replace
        self.raw = raw

    def __call__(self, *args, **kwargs):
        if not NET_INITTED:
            return self.raw(*args, **kwargs)
        # for stack in traceback.walk_stack(None):
        #     if 'self' in stack[0].f_locals:
        #         layer = stack[0].f_locals['self']
        #         if layer in layer_names:
        #             log.pytorch_layer_name = layer_names[layer]
        #             print(layer_names[layer])
        #             break
        out = self.obj(self.raw, *args, **kwargs)
        return out


F.conv2d = Rp(F.conv2d, _conv2d)
F.linear = Rp(F.linear, _linear)
F.relu = Rp(F.relu, _relu)
F.hardtanh = Rp(F.hardtanh, _hardtanh)
torch.sigmoid = Rp(torch.sigmoid, _sigmoid)
F.leaky_relu = Rp(F.leaky_relu, _leaky_relu)
F.max_pool2d = Rp(F.max_pool2d, _max_pool2d)
F.avg_pool2d = Rp(F.avg_pool2d, _avg_pool2d)
F.adaptive_avg_pool2d = Rp(F.adaptive_avg_pool2d, _adaptive_avg_pool2d)
F.adaptive_max_pool2d = Rp(F.adaptive_max_pool2d, _adaptive_max_pool2d)
F.dropout = Rp(F.dropout, _dropout)
F.threshold = Rp(F.threshold, _threshold)
F.prelu = Rp(F.prelu, _prelu)
F.batch_norm = Rp(F.batch_norm, _batch_norm)
F.instance_norm = Rp(F.instance_norm, _instance_norm)
F.softmax = Rp(F.softmax, _softmax)
F.conv_transpose2d = Rp(F.conv_transpose2d, _conv_transpose2d)
F.interpolate = Rp(F.interpolate, _interpolate)
F.max_unpool2d = Rp(F.max_unpool2d, _upsample)

torch.split = Rp(torch.split, _split)
torch.max = Rp(torch.max, _max)
torch.cat = Rp(torch.cat, _cat)

# layers.l2norm.F_L2Norm = Rp(layers.l2norm.F_L2Norm, _l2norm)

raw_view = t.view
t.view = _view
raw_reshape = t.reshape
t.reshape = _reshape
raw_mean = t.mean
t.mean = _mean
raw_permute = t.permute
t.permute = _permute
raw_contiguous = t.contiguous
t.contiguous = _contiguous
raw_faltten = t.flatten
t.flatten = _flatten
raw__add__ = t.__add__
t.__add__ = _add
raw__iadd__ = t.__iadd__
t.__iadd__ = _iadd
raw__sub__ = t.__sub__
t.__sub__ = _sub
raw_isub__ = t.__isub__
t.__isub__ = _isub
raw__mul__ = t.__mul__
# t.__mul__ = _mul
raw__imul__ = t.__imul__
# t.__imul__ = _imul


def trans_net(net, input_var, view2flatten=True, flatten2view=False, relu6torelu=False, name='TransferedPytorchModel'):
    print('Starting Transform, This will take a while')
    log.init([input_var])
    log.cnet.net.name = name
    log.cnet.net.input.extend([log.blobs(input_var)])
    log.cnet.net.input_dim.extend(input_var.size())
    global NET_INITTED
    NET_INITTED = True
    global VIEW2FLATTEN
    VIEW2FLATTEN = view2flatten
    global FLATTEN2VIEW
    FLATTEN2VIEW = flatten2view
    global RELU6TORELU
    RELU6TORELU = relu6torelu
    for name, layer in net.named_modules():
        print(name, layer)
        layer_names[layer] = name
    net.forward(input_var)
    print('Transform Completed')

def parse_prototxt_input(save_path):
    with open(save_path, 'r+') as f:
        file_data = f.readlines()
        new_data = []
        old_input_style = False
        last_parse_input = False
        for line in file_data:
            if 'input_dim' in line:
                last_parse_input = True
                # 起始填充
                if not old_input_style:
                    new_data.append('input_shape {\n')
                    old_input_style = True
                    print("Input express is old style, try reconstruct.")
                dim_number = re.findall(r'\d+', line)
                if len(dim_number) != 1:
                    print("Input express new style reconstruct failed")
                    return
                else:
                    dim_number_str = dim_number[0]
                    new_data.append("  dim: " + dim_number_str + '\n')
            else:
                if last_parse_input:
                    new_data.append('}\n')
                    last_parse_input = False
                new_data.append(line)
        if old_input_style:
            # 清空文件
            f.seek(0)
            f.truncate()
            f.writelines(new_data)
            print("Input express new style reconstruct successfully.")

def save_prototxt(save_path):
    log.cnet.save_prototxt(save_path)
    parse_prototxt_input(save_path)

def save_caffemodel(save_path):
    log.cnet.save(save_path)
