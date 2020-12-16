# coding: utf-8
# Author: wanhui0729@gmail.com

import cv2
import numpy as np

# 构造图像
image = np.zeros([224, 224, 3])
image[100: 150, 100: 150, :] = 255
image = image.astype(np.uint8)

# 需要进行灰度转换
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 找轮廓
contours, hierarchy = cv2.findContours(
    gray,
    mode=cv2.RETR_EXTERNAL,
    method=cv2.CHAIN_APPROX_SIMPLE
)

print("contours: {}".format(contours))
print("hierarchy: {}".format(hierarchy))

# 画出轮廓
cv2.drawContours(image, contours, -1, (0, 0, 255), 2)

cv2.imshow('', image)
cv2.waitKey()