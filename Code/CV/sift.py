# coding: utf-8
# Author: wanhui0729@gmail.com

import cv2
import numpy as np

img = cv2.imread('/data/datasets/coco/2017/train2017/000000000165.jpg')
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# SURF 快速sift版本
# decriptor = cv2.xfeatures2d.SURF_create()
# ORB 结合Fast与Brief算法,更快
# decriptor = cv2.xfeatures2d.ORB_create()
# 128代表查找的关键点个数
descriptor = cv2.xfeatures2d.SIFT_create(128)
# 找到关键点
kp = descriptor.detect(img1, None)
# 绘制关键点
img1_keypoints = cv2.drawKeypoints(img1, kp, img)
cv2.imshow('sp', img1_keypoints)
cv2.waitKey()

# 计算关键点描述符, kp为关键点列表, des为numpy数组, 大小为(len(kp), 128)
kp1, des1 = descriptor.compute(img1, kp)
print(des1.shape)

img2 = cv2.rotate(img1, cv2.ROTATE_90_CLOCKWISE)
# 直接计算
kp2, des2 = descriptor.detectAndCompute(img2, None)
print(des2.shape)

# 特征点匹配, BF
bf = cv2.BFMatcher()
# k代表最匹配的k的点
matches = bf.knnMatch(des1, des2, k=3)
good = []
for m, n in matches:
    # 保证模糊的第二特征点与之匹配
    if m.distance < 0.75 * n.distance:
        good.append([m])
img_match = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, flags=2)
cv2.imshow('match', img_match)
cv2.waitKey()