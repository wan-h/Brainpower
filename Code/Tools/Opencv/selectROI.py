# coding: utf-8
# Author: wanhui0729@gmail.com

import cv2
import numpy as np

image = np.ones((512, 512, 3)) * 255

if __name__ == '__main__':
    while True:
        cv2.imshow('', image)
        key = cv2.waitKey() & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            rois = cv2.selectROIs('', image)
            # xmin ymin w h
            for roi in rois:
                x, y, w, h = roi
                bbox = [int(x), int(y), int(x + w), int(y + h)]
                print(bbox)
        else:
            pass
