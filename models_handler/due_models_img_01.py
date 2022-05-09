# -*-coding:utf-8-*-
import cv2
import numpy as np
from pathlib import Path
import shutil

def green(raw_data='sulige_0304/', out_data='NewData/', ADJUST=100, light=10):
    shutil.copytree(raw_data, out_data, dirs_exist_ok=True)
    for img_p in Path(out_data).rglob('*.jpg'):
        img = cv2.imread(str(img_p))

        b, g, r = cv2.split(img)
        # g[np.logical_and(g > 0, g < 255 - ADJUST)] += ADJUST
        g += ADJUST
        # r[r > 255-ADJUST-ADJUST] -= ADJUST
        # b[b > 255-ADJUST-ADJUST] -= ADJUST
        merged = cv2.merge([b, g, r])
        merged += light
        cv2.imwrite(str(img_p), merged)
        # cv2.imshow('after', merged)
        # cv2.imshow('raw', img)
        # cv2.waitKey()

if __name__ == '__main__':
    green()
