```
  ██████╗   ██████╗  ██████╗██   ██╗
 ██╔═══██╗ ██╔═══██╗██╔════╝██ ██╔═╝
 ███████╔╝ ██║   ██║██║     ████╔╝
 ██╔═██╔╝  ██║   ██║██║     ██╔██═╗
 ██║ ╚═██╗ ╚██████╔╝╚██████╗██║ ╚██╗
 ╚═╝   ╚═╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝
```

# pytorch to caffe tool

## Support layers
from torch import Tensor as t  
import torch.nn.functional as F
* F.conv2d
* F.linear
* F.relu
* F.leaky_relu
* F.max_pool2d
* F.avg_pool2d
* F.dropout
* F.threshold
* F.prelu
* F.batch_norm
* F.instance_norm
* F.softmax
* F.conv_transpose2d
* F.interpolate
* torch.split
* torch.max
* torch.cat
* t.view
* t.mean
* t.permute
* t.contiguous
* t.flatten

## Resource:
* caffe support layer parameter path:
    caffe_install_path/src/caffe/proto/caffe.proto

## Notice:
Do not support layer(caffe):
1. AdaptiveAvgPool

Different implementation:
1. MaxPool (the different implementation that ceil mode in caffe and the floor mode in pytorch)
2. View (the dim[0] should be 0, present batch_size dim)


