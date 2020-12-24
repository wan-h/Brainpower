# coding: utf-8
# Author: wanhui0729@gmail.com

# from __future__ import print_function
import caffe
import pickle
# GPU_ID = 0 # Switch between 0 and 1 depending on the GPU you want to use.
# caffe.set_mode_cpu()
# caffe.set_device(GPU_ID)
from datetime import datetime
import numpy as np
import struct
import sys, getopt
import cv2, os, re
import pickle as p
import matplotlib.pyplot as pyplot
import ctypes
import codecs


def image_to_array(img_file, shape_c_h_w, output_dir):
    result = np.array([])
    print("converting begins ...")
    resizeimage = cv2.resize(cv2.imread(img_file), (shape_c_h_w[2], shape_c_h_w[1]))
    b, g, r = cv2.split(resizeimage)
    height, width, channels = resizeimage.shape
    length = height * width
    # print(channels )
    r_arr = np.array(r).reshape(length)
    g_arr = np.array(g).reshape(length)
    b_arr = np.array(b).reshape(length)
    image_arr = np.concatenate((r_arr, g_arr, b_arr))
    result = image_arr.reshape((1, length * 3))
    print("converting finished ...")
    file_path = os.path.join(output_dir, "test_input_img_%d_%d_%d.bin" % (channels, height, width))
    with open(file_path, mode='wb') as f:
        p.dump(result, f)
    print("save bin file success")


def image_to_bin(img_file, shape_c_h_w, output_dir):
    print("converting begins ...")
    # image = cv2.imread(img_file)
    image = cv2.imdecode(np.fromfile(img_file, dtype=np.uint8), 1)
    image = cv2.resize(image, (shape_c_h_w[2], shape_c_h_w[1]))
    image = image.astype('uint8')
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    file_path = os.path.join(output_dir, "test_input_img_%d_%d_%d.bin" % (channels, height, width))
    fileSave = open(file_path, 'wb')
    for step in range(0, height):
        for step2 in range(0, width):
            fileSave.write(image[step, step2, 2])
    for step in range(0, height):
        for step2 in range(0, width):
            fileSave.write(image[step, step2, 1])
    for step in range(0, height):
        for step2 in range(0, width):
            fileSave.write(image[step, step2, 0])

    fileSave.close()
    print("converting finished ...")


def bin_to_image(bin_file, shape_c_h_w):
    # fileReader = open(bin_file,'rb', encoding='utf-8')
    fileReader = open(bin_file.encode('gbk'), 'rb')
    height = shape_c_h_w[1]
    width = shape_c_h_w[2]
    channel = shape_c_h_w[0]
    imageRead = np.zeros((shape_c_h_w[1], shape_c_h_w[2], shape_c_h_w[0]), np.uint8)
    for step in range(0, height):
        for step2 in range(0, width):
            a = struct.unpack("B", fileReader.read(1))
            imageRead[step, step2, 2] = a[0]
    for step in range(0, height):
        for step2 in range(0, width):
            a = struct.unpack("B", fileReader.read(1))
            imageRead[step, step2, 1] = a[0]
    for step in range(0, height):
        for step2 in range(0, width):
            a = struct.unpack("B", fileReader.read(1))
            imageRead[step, step2, 0] = a[0]
    fileReader.close()
    return imageRead


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_float_numbers(floatfile):
    mat = []
    with open(floatfile.encode('gbk'), 'rb') as input_file:
        for line in input_file:
            line = line.strip()
            for number in line.split():
                if isfloat(number):
                    mat.append(float(number))
    return mat


def isHex(value):
    try:
        int(value, 16)
        return True
    except ValueError:
        return False


def isHex_old(value):
    strvalue = str(value)
    length = len(strvalue)
    if length == 0:
        return False
    i = 0
    while (i < length):
        if not (strvalue[i] >= 'a' and strvalue[i] <= 'e' or strvalue[i] >= 'A' and strvalue[i] <= 'E' or strvalue[
            i] >= '0' and strvalue[i] <= '9'):
            return False
        i += 1
    return True


def get_hex_numbers(hexfile):
    mat = []
    with open(hexfile.encode("gbk")) as input_file:
        for line in input_file:
            line = line.strip()
            for number in line.split():
                if isHex(number):
                    mat.append(1.0 * ctypes.c_int32(int(number, 16)).value / 4096)
    return mat


def print_CNNfeaturemap(net, output_dir):
    params = list(net.blobs.keys())
    print(params)
    for pr in params[0:]:
        print(pr)
        res = net.blobs[pr].data[...]
        pr = pr.replace('/', '_')
        print(res.shape)
        for index in range(0, res.shape[0]):
            if len(res.shape) == 4:
                filename = os.path.join(output_dir, "%s_output%d_%d_%d_%d_caffe.linear.float" % (
                pr, index, res.shape[1], res.shape[2], res.shape[3]))
            elif len(res.shape) == 3:
                filename = os.path.join(output_dir, "%s_output%d_%d_%d_caffe.linear.float" % (
                pr, index, res.shape[1], res.shape[2]))
            elif len(res.shape) == 2:
                filename = os.path.join(output_dir, "%s_output%d_%d_caffe.linear.float" % (pr, index, res.shape[1]))
            elif len(res.shape) == 1:
                filename = os.path.join(output_dir, "%s_output%d_caffe.linear.float" % (pr, index))
            f = open(filename, 'wb')

            # np.savetxt(f, list(res.reshape(-1, 1)))
            reshape_data = res.reshape(-1, 1)
            data_list = reshape_data.squeeze().tolist()
            with open(filename, 'w') as f:
                for data in data_list:
                    f.writelines("{:.18f}\n".format(data))

def genWeightsFile(model_file,
               weight_file,
               input_file,
               norm_type=5,
               data_scale=1.0,
               data_mean=[103.94, 116.78, 123.68],
               output_dir='featureMaps_output'):
    '''
    Arguments:
        model_file: .prototxt, batch num should be 1
        weight_file: .caffemodel
        imput_file: .JPEG or jpg or png or PNG or bmp or BMP
        norm_type: 0(default): no process, 1: sub img-val and please give the img path in the parameter p, 2: sub channel mean value and please give each channel value in the parameter p in BGR order, 3: dividing 256, 4: sub mean image file and dividing 256, 5: sub channel mean value and dividing 256
        data_scale: optional, if not set, 1.0 is set by default
        data_mean: default([103.94, 116.78, 123.68])
        output_dir: optional, if not set, there will be a directory named output created in current dir
    return:
        None
    '''
    print('model file is: ', model_file)
    print('weight file is: ', weight_file)
    print('input file is: ', input_file)
    print('image preprocessing method is: ', norm_type)  # default is no process
    print('data mean is :', data_mean)
    print('data scale is: ', data_scale)
    print('output dir is: ', output_dir)
    net = caffe.Net(model_file.encode('gbk'), weight_file.encode('gbk'), caffe.TEST)
    print('model load success...')

    if norm_type == '1' or norm_type == '4':
        meanfile = data_mean
        if not os.path.isfile(meanfile):
            print("Please give the mean image file path")
            sys.exit(1)
        if meanfile.endswith('.binaryproto'):
            meanfileBlob = caffe.proto.caffe_pb2.BlobProto()
            meanfileData = open(meanfile.encode('gbk'), 'rb').read()
            meanfileBlob.ParseFromString(meanfileData)
            arr = np.array(caffe.io.blobproto_to_array(meanfileBlob))
            out = arr[0]
            np.save('transMean.npy', out)
            meanfile = 'transMean.npy'
    # if norm_type == '2' or norm_type == '5':
    # print('meanshape:') 
    # lmeanfile=meanfile.split(',')
    # if not isfloat(lmeanfile[0]) or not isfloat(lmeanfile[1]) or not isfloat(lmeanfile[2]): 
    #   print("Please give the channel mean value in BGR order") 
    #   sys.exit(1)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    if input_file.endswith('.jpg') or input_file.endswith('.png') or input_file.endswith(
            '.jpeg') or input_file.endswith('.bmp') or input_file.endswith('.JPEG') or input_file.endswith(
            '.PNG') or input_file.endswith('.JPG') or input_file.endswith('.BMP'):
        image_to_bin(input_file, net.blobs['data'].data.shape[1:], output_dir)
        if net.blobs['data'].data.shape[1] == 1:
            color = False
        elif net.blobs['data'].data.shape[1] == 3:
            color = True
        img = cv2.imdecode(np.fromfile(input_file, dtype=np.uint8), -1)
        # img = cv2.imread(input_file, color) # load the image using caffe io
        inputs = img
    elif input_file.endswith('.bin'):
        fbin = open(input_file.encode('gbk'))
        data = bin_to_image(input_file, net.blobs['data'].data.shape[1:])
        inputs = data
    elif input_file.endswith('.float'):
        data = np.asarray(get_float_numbers(input_file))
        inputs = data
        inputs = np.reshape(inputs, net.blobs[list(net.blobs.keys())[0]].data.shape)
    elif input_file.endswith('.hex'):
        data = np.asarray(get_hex_numbers(input_file))
        inputs = data
        inputs = np.reshape(inputs, net.blobs[list(net.blobs.keys())[0]].data.shape)
    else:
        print("errors: unknown input file!")
        sys.exit(1)

    if len(inputs):
        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
        if net.blobs['data'].data.shape[1] == 3:
            transformer.set_transpose('data', (2, 0, 1))
        if norm_type == '1' or norm_type == '4' and os.path.isfile(meanfile):  # (sub mean by meanfile):
            if net.blobs['data'].data.shape[1] == 3:
                transformer.set_mean('data', np.load(meanfile).mean(1).mean(1))
            elif net.blobs['data'].data.shape[1] == 1:
                tempMeanValue = np.load(meanfile).mean(1).mean(1)
                tempa = list(tempMeanValue)
                inputs = inputs - np.array(list(map(float, [tempa[0]])))
        elif norm_type == '2' or norm_type == '5':
            if net.blobs['data'].data.shape[1] == 3:
                lmeanfile = meanfile.split(',')
                if len(lmeanfile) != 3:
                    print("Please give the channel mean value in BGR order with 3 values, like 112,113,120")
                    sys.exit(1)
                if not isfloat(lmeanfile[0]) or not isfloat(lmeanfile[1]) or not isfloat(lmeanfile[2]):
                    print("Please give the channel mean value in BGR order")
                    sys.exit(1)
                else:
                    transformer.set_mean('data', np.array(list(map(float, re.findall(r'[-+]?\d*\.\d+|\d+', meanfile)))))
            elif net.blobs['data'].data.shape[1] == 1:
                lmeanfile = meanfile.split(',')
                if isfloat(lmeanfile[0]):  # (sub mean by channel)
                    inputs = inputs - np.array(list(map(float, [lmeanfile[0]])))

        elif norm_type == '3':
            inputs = inputs * float(data_scale)
        if input_file.endswith('.txt') or input_file.endswith('.float') or input_file.endswith('.hex'):
            print(inputs.shape)
            data = inputs
        else:
            data = np.asarray([transformer.preprocess('data', inputs)])
        if norm_type == '4' or norm_type == '5':
            data = data * float(data_scale)

    data_reshape = np.reshape(data, net.blobs[list(net.blobs.keys())[0]].data.shape)
    net.blobs[list(net.blobs.keys())[0]].data[...] = data_reshape.astype('float')
    out = net.forward()

    print_CNNfeaturemap(net, output_dir)
    sys.exit(0)