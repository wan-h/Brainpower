# coding: utf-8
# Author: wanhui0729@gmail.com

import cv2

# 初始化
videoCapture = cv2.VideoCapture('/data/test.MOV')


# 获取fps
fps = int(videoCapture.get(cv2.CAP_PROP_FPS))
print(f"Video fps: {fps}")
# 获取size
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(f"Video size: {size}")

# 当前几种编码格式
# CV_FOURCC('P', 'I', 'M', '1') = MPEG-1
# CV_FOURCC('M', 'J', 'P', 'G') = motion-jpeg
# CV_FOURCC('M', 'P', '4', '2') = MPEG-4.2
# CV_FOURCC('D', 'I', 'V', '3') = MPEG-4.3
# CV_FOURCC('D', 'I', 'V', 'X') = MPEG-4
# CV_FOURCC('U', '2', '6', '3') = H263
# CV_FOURCC('I', '2', '6', '3') = H263I
# CV_FOURCC('F', 'L', 'V', '1') = FLV1
# CV_FOURCC('A', 'V', 'C', '1') =  H264
fourcc = cv2.VideoWriter_fourcc(*'AVC1')
# 初始化
videoWriter = cv2.VideoWriter('test.mp4', fourcc, fps, size)

# 读取视频
success, frame = videoCapture.read()
while success:
    cv2.imshow('video frame', frame)
    cv2.waitKey()
    # 写入
    videoWriter.write(frame)
    # 继续读取
    success, frame = videoCapture.read()

# 释放
videoCapture.release()
videoWriter.release()
