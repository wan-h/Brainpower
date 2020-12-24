# coding: utf-8
# Author: wanhui0729@gmail.com

'''
compare two images
'''

from sklearn import metrics as mr
from skimage.measure import compare_ssim
from scipy.misc import imread
from PIL import Image
import numpy as np
from numpy import average, linalg, dot
from functools import reduce
import cv2

def image_compare_ssim(img1, img2):
    '''
    SSIM structure similarity
    :param img1: image path
    :param img2: image path
    :return: ssim similarity value
    '''
    img1 = imread(img1)
    img2 = imread(img2)
    img2 = np.resize(img2, (img1.shape[0], img1.shape[1], img1.shape[2]))
    ssim = compare_ssim(img1, img2, multichannel=True)
    return ssim

def image_compare_cosin(img1, img2):
    '''
    cosin similarity
    :param img1: image path
    :param img2: image path
    :return: cosin similarity value
    '''
    def get_thumbnail(image, size, greyscale=False):
        image = image.resize(size, Image.ANTIALIAS)
        if greyscale:
            image = image.convert('L')
        return image

    def image_similarity_vectors_via_numpy(image1, image2):
        image1 = get_thumbnail(image1, image1.size)
        image2 = get_thumbnail(image2, image1.size)
        images = [image1, image2]
        vectors = []
        norms = []
        for image in images:
            vector = []
            for pixel_tuple in image.getdata():
                vector.append(average(pixel_tuple))
            vectors.append(vector)
            norms.append(linalg.norm(vector, 2))
        a, b = vectors
        a_norm, b_norm = norms
        res = dot(a / a_norm, b / b_norm)
        return res

    img1 = Image.open(img1)
    img2 = Image.open(img2)
    cosin = image_similarity_vectors_via_numpy(img1, img2)
    return cosin

def image_compare_hist(img1, img2):
    '''
    hist similarity
    :param img1: image path
    :param img2: image path
    :return: hist similarity value
    '''
    def make_regalur_image(img, size):
        return img.resize(size).convert('RGB')

    def hist_similar(lh, rh):
        assert len(lh) == len(rh)
        return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

    def calc_similar(li, ri):
        return hist_similar(li.histogram(), ri.histogram())

    img1 = Image.open(img1)
    img1 = make_regalur_image(img1, img1.size)
    img2 = Image.open(img2)
    img2 = make_regalur_image(img2, img1.size)
    value = calc_similar(img1, img2)
    return value

# 基于互信息
def image_compare_mutualInfo(img1, img2):
    '''
    mutual info similarity
    :param img1: image path
    :param img2: image path
    :return: mutual info similarity value
    '''
    img1 = imread(img1)
    img2 = imread(img2)

    img2 = np.resize(img2, (img1.shape[0], img1.shape[1], img1.shape[2]))

    img1 = np.reshape(img1, -1)
    img2 = np.reshape(img2, -1)
    mutual_infor = mr.mutual_info_score(img1, img2)
    return mutual_infor

def image_compare_hash(img1, img2):
    '''
    hash similarity
    :param img1: image path
    :param img2: image path
    :return: hash similarity value
    '''
    def phash(img):
        """
        :param img: 图片
        :return: 返回图片的局部hash值
        """
        img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
        hash_value = reduce(lambda x, y: x | (y[1] << y[0]), enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())), 0)
        return hash_value

    # 计算汉明距离:
    def hamming_distance(a, b):
        """
        :param a: 图片1的hash值
        :param b: 图片2的hash值
        :return: 返回两个图片hash值的汉明距离
        """
        hm_distance = bin(a ^ b).count('1')
        return hm_distance

    img1 = Image.open(img1)
    img2 = Image.open(img2)
    distance = hamming_distance(phash(img1), phash(img2))
    return distance

# pip install opencv-contrib-python==3.4.1.15
def image_compare_sift(img1, img2):
    '''
    sift similarity
    :param img1: image path
    :param img2: image path
    :return: sift similarity value
    '''
    def getMatchNum(matches, ratio):
        '''返回特征点匹配数量和匹配掩码'''
        matchesMask = [[0, 0] for i in range(len(matches))]
        matchNum = 0
        for i, (m, n) in enumerate(matches):
            if m.distance < ratio * n.distance: #将距离比率小于ratio的匹配点删选出来
                matchesMask[i] = [1,0]
                matchNum += 1
        return (matchNum, matchesMask)

    #创建SIFT特征提取器
    sift = cv2.xfeatures2d.SIFT_create()
    #创建FLANN匹配对象
    FLANN_INDEX_KDTREE = 0
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)

    img1 = cv2.imread(img1, 0)
    img2 = cv2.imread(img2, 0)
    kp1, des1 = sift.detectAndCompute(img1, None) #提取样本图片的特征
    kp2, des2 = sift.detectAndCompute(img2, None)

    #匹配特征点，为了删选匹配点，指定k为2，这样对样本图的每个特征点，返回两个匹配
    matches=flann.knnMatch(des1, des2, k=2)
    #通过比率条件，计算出匹配程度
    (matchNum, matchesMask) = getMatchNum(matches,0.9)

    matchRatio = matchNum * 100 / len(matches)
    return matchRatio