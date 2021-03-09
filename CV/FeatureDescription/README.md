## Feature Description
### SIFT
[参考](https://www.cnblogs.com/pacino12134/p/11368558.html)  
SIFT的全称是Scale Invariant Feature Transform，尺度不变特征变换，由加拿大教授David G.Lowe提出的用于提取图像中不变的特征。
SIFT特征对旋转、尺度缩放、亮度变化等保持不变性，是一种非常稳定的局部特征。  
计算步骤:  
* 构建尺度空间  
* 得到初始关键点(查找极值点)  
* 提高关键点位置的精度  
* 删除不合适的关键点  
* 计算关键点方向  
* 计算关键点描述子
### HOG
[参考1](https://zhuanlan.zhihu.com/p/85829145)  
[参考2](https://www.jianshu.com/p/44bd4473da65)  
SIFT的全称是Histogram Orientated Graphic，方向梯度直方图，通过计算和统计图像局部区域的梯度方向直方图来构成特征。  
计算步骤:  
* 图像归一化  
* 利用一阶微分计算图像梯度  
* 基于梯度幅值的方向权重投影
* HOG特征向量归一化  
* 得出HOG最终的特征向量