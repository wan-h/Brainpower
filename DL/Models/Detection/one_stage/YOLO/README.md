## YOLO
### YOLOv1
[paper](https://arxiv.org/pdf/1506.02640.pdf)  
[code](http://pjreddie.com/yolo/)  

---
#### STRUCTURE
![](src/Structure_0.png)  

---
#### Experimental Results
* PASCAL VOC2012 test
![](src/ER_0.png)

---
#### Algorithm
* 输出纬度 S * S * (C + B * (4 + 1))  
其中S为输出网格大小，C为目标类别数量，B为在单元网格被预测的框个数，1为当前预测框的置信度。
可理解为网络将图像划分为S * S个网格，然后在每个单元网格去预测B个框位置，每个框预测都包含了xywh四个位置信息以及是否存在目标的置信度。
且同一个网格单元的预测框共享类别预测信息。这也导致了YOLO的局限性，多个预测框有且只能有一个类别，对边界框的预测施加了强大的空间约束。
* 损失函数  
![](src/loss_0.png)  
总的来说，网络输出和样本标签的各项内容的误差平方和作为一个样本的整体误差。
公式1、2行表示框预测误差，目标中心点单元网格的预测框只有IOU比较大的bounding box的数据才会计入误差，
且由于不同大小的对象对差值的敏感程度不同，所以在宽度和高度上取平方根来较低这种敏感度。
公式3、4行表示置信度误差，对于预测框内无对象的置信度误差加了一个权重项。
公式5行表示对象分类误差，只有有对象的网格才计入误差。
* 目标框编解码  
目标框(x, y, w, h)，其中x, y表示目标框中心相对单元网格的边界的距离。w, h则是相对于图像宽高的比值。
* 网络预测  
在预测阶段，最后一个目标可能会被多个网格预测出来，所以通过[NMS](../../../../Algorithm/NMS.md)再做筛选。

---
#### Intuition
You Only Look Once，人们看了一眼图像，立即知道图像中有什么对象，它们在哪里以及它们如何相互作用。
YOLO将候选区和对象识别这两个阶段合二为一，旨在可以进行实时的目标检测。

---
--- 
### YOLOv2
[paper](https://arxiv.org/pdf/1612.08242.pdf)  
[code](http://pjreddie.com/yolo9000/) 

---
#### STRUCTURE
![](src/Structure_1.png)  

---
#### Experimental Results
* PASCAL VOC 2007  
![](src/ER_1.png)
* PASCAL VOC2012 test  
![](src/ER_2.png)
* COCO test-dev2015  
![](src/ER_3.png)

---
#### Algorithm  
* Better  
1.Batch Normalization  
相当于一种正则化手段，提高网络收敛性，更快收敛，最终使得mAP提高2%，而且使得模型的泛化能力更强。  
2.High resolution classifier  
输入尺寸更大的图片224->448，并且将backbone在Imagenet上进行微调，最终使得mAP提高4%。  
3.Convolution with anchor boxes  
YOLOv1使用全连接层直接预测Bounding Boxes的坐标值，借鉴Faster R-CNN的RPN网络，通过预测Anchor Box的
坐标偏移量来简化检测问题。使用416尺寸的输入图像，最终输出13x13的特征图，再在特征图上做Anchor Box的
框回归和类别分类，使用anchor后mAP降低了0.3，但是能够预测出大于一千的预测框，相对于YOLOv1的98个预测框
提高了召回率7%。  
4.Dimension clusters  
Faster R-CNN中使用的Anchor Box都是手动选择的，YOLOv2通过聚类的方式选取出预选框，
其与ground truth的匹配效果优于默认的anchor。  
5.Direct location prediction  
YOLOv2还是像YOLOv1一样，预测框坐标是与网格相关的。假设一个网格的大小是1，
只要在预测框x,y坐标输出之前加一个sigmoid即可让比例在0-1之间，从而让框的中心点限制在一个网格中。  
![](src/Oth_0.png)  
使用聚类Dimension clusters和直接位置预测Direct location prediction的方法，
使YOLO比其他使用Anchor Box的版本提高了近5％。（这里的之所以还是直接位置预测是因为之前的聚类只对
宽高做了一个预选，而v1是直接做的相对于整图宽高做的预测）  
6.Fine-Grained Features  
SSD通过多尺度的特征图来进行预测获取不同的分辨率，YOLOv2仅仅在26x26的特征层上添加了一个passthrough层。
这使 26×26×512 特征层变成 13×13×2048，然后就可以堆叠到后一层特征图上了。  
![](src/Oth_1.png)  
7.Multi-Scale Training  
用不同尺寸的图片训练，区别于之前固定图片尺寸的做法，YOLOv2 每迭代几次都会改变网络，修改最后检测层的处理。
每10个Batch，网络会随机地选择一个新的图片尺寸。由于使用了下采样参数是32，所以不同的尺寸大小也选择为32的倍数
{320，352…..608}（分别是10，11...19倍），最小320×320，最大608×608，网络会自动改变尺寸，并继续训练的过程。  

* Faster  
1.Darknet-19  
![](src/Structure_2.png)  
2.Training for classification预训练  
通过ImageNet1000上进行预训练  
3.Training for detection微调训练  
保证主干网络的权重修改最后一层，新增3个3×3×1024的卷积，再加一个1×1卷积，还加了一个passthrouth层。

* Stronger  
通过WordTree的概念，获得更多的数据来源和数据纬度。  

---
#### Intuition
对YOLO的改进，Better，Faster，Stronger

---
---
### YOLOv3
[paper](https://arxiv.org/pdf/1804.02767.pdf)  
[code](https://pjreddie.com/yolo/) 

---
#### STRUCTURE
![](src/Structure_3.png)  

---
#### Experimental Results
* COCO test-dev2015  
![](src/ER_4.png)

---
#### Algorithm  
* backbone修改为darknet-53  
![](src/Oth_2.png)  
* 类FPN结构  
![](src/Oth_3.png)  
类似SSD的结构，在三个不同尺度的特征图上进行预测  
* 替换Softmax  
分类器Softmax层被替换为一个1x1卷积层＋logistic激活函数的结构，使用Softmax层已经假设输出只对应单个class,但是某些class存在重叠的情况
(例如woman和person的数据集中)，使用Softmax不能对该类数据进行较好的拟合。  

---
#### Intuition  
使用类FPN结构网络，对于小目标等困难目标有更好的检测效果，且在不同特征尺度上进行预测(类似SSD的head部分)，使得小目标可以在较大的特征图上进行预测，
由于网络更加复杂，所有整体耗时上相比v2有所增加。  

--- 
--- 
### YOLOv4  
[paper](https://arxiv.org/pdf/2004.10934.pdf)  
[code](https://github.com/AlexeyAB/darknet)  

---  
#### STRUCTURE  
![](src/Structure_4.png)  

---  
#### Experimental Results  
* COCO test-dev2017  
![](src/ER_5.png)  

---  
#### Algorithm  
###### BoF for backbone
* [CutMix](https://arxiv.org/pdf/1905.04899v2.pdf)  
将一部分区域cut掉但不填充0像素而是随机填充训练集中的其他数据的区域像素值，label结果按照比例分配  
![](src/Oth_10.png)  
* Mosaic data augmentation  
CutMix主要用于分类，Mosaic就是参考CutMix的改进版，用于检测任务中，主要思想就是将四张图片进行裁剪，
再拼接到一张图上作为训练数据，若裁剪了样本中标签框的部分区域就直接将其舍弃  
![](src/Oth_11.png)  
* [DropBlock regularization](https://arxiv.org/pdf/1810.12890.pdf)  
一种针对卷积的正则化，通过dropout掉一部分相邻的整片的区域（比如头和脚），网络就会去注重学习狗的别的部位的特征，
来实现正确分类，从而表现出更好的泛化  
![](src/Oth_12.png)  
* Class label smoothing  
一种正则化的策略，通过soft one-hot来加入噪声，减少了真实样本标签的类别在计算损失函数时的权重，最终起到抑制过拟合的效果，
也配合类似Mixup这类数据增强方法，生成soft label  

###### BoS for backbone
* [Mish activation](https://arxiv.org/pdf/1908.08681.pdf)  
实验结论比relu的效果更好，相比relu处处可导且允许负梯度的传播  
![](src/Oth_13.png)  
* [Cross-stage partial connections(CSP)](https://arxiv.org/pdf/1911.11929.pdf)  
使用CSP结构改造Darknet53，CSPDarknet53    
![](src/Oth_8.png)  
CSP结构将base layer按channel一分为二，保留了denseNet特征重复使用的优点，该结构有三点优势：
1.加强CNN的学习能力(增加了梯度路径); 
2.消除计算瓶颈(输入砍半); 
3.降低内存成本(输入砍半)  
后融合的Transition相当于梯度截断，避免了重复的梯度信息更新不同的dense block权重，使梯度组合的差异最大化
* [Multi-input weighted residual connections(MiWRC)](https://arxiv.org/pdf/1605.08831.pdf)  
修改残差结构,原始结构为  
![](src/Oth_4.png)  
![](src/Oth_5.png)  
新结构为  
![](src/Oth_6.png)  
![](src/Oth_7.png)  
论文中描述Weighted-Residual可以更好更快的结合不同层传递过来的残差，虽然增加了一些计算量，
但是当网络层数从100+增加到1000+时，网络效果更好，收敛速度更快，主要原因在于Relu和残差的加法存在不兼容，
Relu只能输出大于0也就只能增强信号，这限制了残差函数负无穷到正无穷的可表示性，其次将Relu从高速通道移动到
分支通道，保证了高速信号可以畅通传递，也就更好地适应了更深的网络结构  

###### BoF for detector
* CIOU-loss  
使用[IOU 损失](../../../../ModelOperator/DistanceIouLoss/README.md)替代MSE 损失   
* CmBN  
归一化均值方差是前面几个mini-batch均值方差的共同计算，
以此解决batch_size过小时分布统计量不准确的问题
![](src/Oth_9.png)  
* DropBlock regularization  
同BoF for Backbone  
* Mosaic data augmentation  
同BoF for Backbone  
* Self-Adversarial Training  
BP时不调整参数，而是调整image，然后将调整后的imnage加入训练来防止过拟合  
* Eliminate grid sensitivity  
在计算box信息时，若bx=cx or bx=cx+1两种情况需要tx是一个极大的负值或则正值才能使得loss很小，
所以再激活函数σ乘以一个系数，那么产生较小的loss就要容易一些  
![](src/Oth_14.png)  
* Using multiple anchors for a single ground truth  
有可能存在多个anchors和groud truth的IOU大于阈值，每个groud truth对应多个anchor都加入计算，
以往通常的操作是每个groud truth只将最匹配的anchor作为正样本  
* Cosing annealing scheduler  
使用余弦退火调整学习率  
![](src/Oth_15.png)  
* Optimal hyper-parameters  
对于超参数，用类似遗传算法进行分组寻优  
* Random training shapes  
对于image用多shape进行输入，使模型具有更好的通用性  

###### BoS for detector
* Mish activate  
同BoS for Backbone  
* SPP-block  
![](src/Oth_16.jpg)  
* PAN path-aggregation block  
![](src/Oth_17.png)  
* [SAM-block(Spatial Attention Module)](https://arxiv.org/pdf/1807.06521.pdf%22%20%5Ct%20%22https://heartbeat.fritz.ai/_blank)  
![](src/Oth_18.png)  
* [DIoU-NMS](https://arxiv.org/pdf/1911.08287.pdf)  
在进行NMS计算是后，除了通过IOU计算外，增加Box之间的距离信息
![](src/Oth_19.png)  
![](src/Oth_20.png)  

---
#### Intuition  
yolov4是可以说是tricks万花筒，可以看做是目标检测模型tricks文献综述，将大量的炼丹技巧应用到了论文中  

--- 
--- 
### YOLOv5  
[paper]()  
[code](https://github.com/ultralytics/yolov5)  

---  
#### STRUCTURE  
![](src/Structure_5.png)  

---  
#### Experimental Results  
* COCO test-dev2017  
![](src/ER_6.png)  

---  
#### Algorithm  

---
#### Intuition  