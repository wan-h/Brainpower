# coding: utf-8
# Author: wanhui0729@gmail.com

'''
透视变换
相较于
'''

import cv2
import numpy as np

# 构造图像
image = np.ones([224, 224, 3]) * 255
image[100: 150, 100: 150, :] = 0
image = image.astype(np.uint8)
rows, cols, _ = image.shape

# 通过getPerspectiveTransform获取变换矩阵
points1 = np.float32([[100, 100], [150, 100], [150, 150], [100, 150]])
points2 = np.float32([[100, 100], [150, 100], [100, 150], [60, 150]])
# 只支持四个points作为输入
matrix = cv2.getPerspectiveTransform(points1, points2)
print(matrix.shape)
image1 = cv2.warpPerspective(image, matrix, (cols, rows))
cv2.imshow('image', image)
cv2.imshow('image1', image1)
cv2.waitKey()