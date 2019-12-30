## MobileNet
### MobileNetv1
[paper](https://arxiv.org/pdf/1506.02640.pdf)  
[code](http://pjreddie.com/yolo/)  

---
#### STRUCTURE
![](src/Structure_0.png)  

---
#### Experimental Results
* ImageNet  
![](src/ER_0.png)  
![](src/ER_1.png)  
* Face Attributes  
![](src/ER_2.png)  
* Face Embeddings  
![](src/ER_3.png)  
* Object Detection(COCO)  
![](src/ER_4.png)

---
#### Algorithm
* 深度可分离据卷积（Depthwise Separable Convolution）  
![](src/Oth_0.png)  
深度可分离卷积将标准卷积分解为depthwise convolution和pointwise convolution，
depthwise convolution将单个滤波器应用到每个输入通道，所以深度卷积的数量和通道数保持一致。
pointwise convolution再通过1x1的卷积将深度卷积的输出组合起来，其通道数为特征图通道数，个数为输出通道数。  
深度可分离卷积和标准卷积计算成本比值为：  
![](src/Oth_1.png)  
一层标准的卷积结构可以通过一层深度卷积和一层逐点卷积代替：  
![](src/Oth_2.png)  
* 宽度乘数（Width Multiplier）  
宽度乘数作用于每一层的通道数上，对于给定的层和宽度乘数α，输入通道M的数量变为αM，输出通道数量N变为αN。  
可分离卷积计算成本变为：  
![](src/Oth_3.png)  
* 分辨率乘数  
分辨率乘数应用于输入图像，并且每个特征层的内部表示随后通过相同的乘法器减少。  
若设置输入分辨率乘数为ρ,可分离卷积计算成本变为：  
![](src/Oth_4.png)

---
#### Intuition  
专门针对移动设备和嵌入式设备提出的网络，通过特殊的设计来构建轻量级的深度神经网络
且通过两个简单的全局超参数来折中模型的性能。

### MobileNetv2
[paper]()  
[code]() 

---
#### STRUCTURE


---
#### Experimental Results

---
#### Algorithm  

---
#### Intuition


### MobileNetv3
[paper]()  
[code]() 

---
#### STRUCTURE


---
#### Experimental Results

---
#### Algorithm  
