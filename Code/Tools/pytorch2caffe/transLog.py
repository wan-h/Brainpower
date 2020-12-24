# coding: utf-8
# Author: wanhui0729@gmail.com

from .Caffe import caffe_net


class Blob_LOG():
    def __init__(self):
        self.data = {}
    def __setitem__(self, key, value):
        self.data[key] = value
    def __getitem__(self, key):
        return self.data[key]
    def __len__(self):
        return len(self.data)

class TransLog(object):
    def __init__(self):
        """
        doing init() with inputs Variable before using it
        blob is operation of pytorch's output
        detail name = name + count
        """
        # record model layers, {detail_layers name: detail_layers name}
        self.layers = {}
        # count the same type layers and rename with +1 count, {layers name: count}
        self.detail_layers = {}
        # count the same type blobs and rename with +1 count, {blobs name: count}
        self.detail_blobs = {}
        # record blobs, {id(blob): detail_blobs name}
        self._blobs = Blob_LOG()
        # record blobs
        self._blobs_data = []
        # build caffe model
        self.cnet = caffe_net.Caffemodel('')
        self.debug = True

    def init(self, inputs):
        """
        Arguments:
            inputs: is a list of input variables
        """
        self.add_blobs(inputs, name='data', with_num=False)

    def add_layer(self, name='layer'):
        if name in self.layers:
            return self.layers[name]
        if name not in self.detail_layers.keys():
            self.detail_layers[name] = 0
        self.detail_layers[name] += 1
        name = '{}{}'.format(name, self.detail_layers[name])
        self.layers[name] = name
        if self.debug:
            print("{} was added to layers".format(self.layers[name]))
        return self.layers[name]

    def add_blobs(self, blobs, name='blob', with_num=True):
        rst = []
        for blob in blobs:
            self._blobs_data.append(blob)
            blob_id = int(id(blob))
            if name not in self.detail_blobs.keys():
                self.detail_blobs[name] = 0
            self.detail_blobs[name] += 1
            if with_num:
                rst.append('{}{}'.format(name, self.detail_blobs[name]))
            else:
                rst.append('{}'.format(name))
            if self.debug:
                print("{}:{} was added to blobs".format(blob_id, rst[-1]))
            print('Add blob {} : {}'.format(rst[-1].center(21), blob.size()))
            self._blobs[blob_id] = rst[-1]
        return rst

    def blobs(self, var):
        var = id(var)
        if self.debug:
            print("{}:{} getting".format(var, self._blobs[var]))
        try:
            return self._blobs[var]
        except:
            print("WARNING: CANNOT FOUND blob {}".format(var))
            return None