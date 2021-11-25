# coding: utf-8
# Author: wanhui0729@gmail.com

'''
仿射变换
仿射变换通过一系列原子变换复合实现，具体包括：平移（Translation）、缩放（Scale）、旋转（Rotation）、翻转（Flip）和错切（Shear）
'''

import cv2
import numpy as np

# 构造图像
image = np.ones([224, 224, 3]) * 255
image[100: 150, 100: 150, :] = 0
image = image.astype(np.uint8)
rows, cols, _ = image.shape

# 通过getRotationMatrix2D获取变换矩阵
# 得到变换的矩阵，通过这个矩阵再利用warpAffine来进行变换
# 第一个参数就是旋转中心，元组的形式，这里设置成相片中心
# 第二个参数90，是旋转的角度
# 第三个参数1，表示放缩的系数，1表示保持原图大小
matrix = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
image1 = cv2.warpAffine(image, matrix, (cols, rows))
print(matrix.shape)
cv2.imshow('image', image)
cv2.imshow('image1', image1)

# 通过getAffineTransform获取变换矩阵
points1 = np.float32([[100, 100], [150, 100], [150, 150]])
points2 = np.float32([[100, 100], [150, 100], [100, 150]])
# 只支持三个points作为输入
matrix = cv2.getAffineTransform(points1, points2)
print(matrix.shape)
image2 = cv2.warpAffine(image, matrix, (cols, rows))
cv2.imshow('image2', image2)
cv2.waitKey()