# coding: utf-8
# Author: wanhui0729@gmail.com

import cv2
import torch
import numpy as np


yuv_from_rgb = np.array([[0.299,       0.587,       0.114],
                         [-0.14714119, -0.28886916, 0.43601035],
                         [0.61497538,  -0.51496512, -0.10001026]])

def np_rgb2yuv(img):
    img = img @ yuv_from_rgb.T.astype(img.dtype)
    img[..., 1] += 128
    img[..., 2] += 128
    print(img)
    return img

def torch_rgb2yuv(img):
    k_yuv_from_rgb = torch.from_numpy(yuv_from_rgb.T).float()
    img = torch.from_numpy(img).float()
    img = torch.matmul(img, k_yuv_from_rgb)
    img[..., 1] += 128
    img[..., 2] += 128
    print(img)
    return img.numpy()

if __name__ == '__main__':
    img = cv2.imread('/data/datasets/animegan/Shinkai/test/real/22.jpg')
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_yuv_cv2 = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv_np = np_rgb2yuv(img_rgb.astype(np.floating)).astype(np.uint8)
    img_yuv_torch = torch_rgb2yuv(img_rgb.astype(np.floating)).astype(np.uint8)
    batch = np.stack([img_rgb.astype(np.floating) for _ in range(2)])
    img_yuv_torch_batch = torch_rgb2yuv(batch).astype(np.uint8)
    img_yuv_torch_batch = img_yuv_torch_batch[0]

    cv2.imshow("img_yuv_cv2", img_yuv_cv2)
    cv2.imshow("img_yuv_np", img_yuv_np)
    cv2.imshow("img_yuv_torch", img_yuv_torch)
    cv2.imshow("img_yuv_torch_batch", img_yuv_torch_batch)
    cv2.waitKey()