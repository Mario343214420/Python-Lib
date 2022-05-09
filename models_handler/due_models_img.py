# -*-coding:utf-8-*-
import cv2
import numpy as np
from pathlib import Path
import shutil
from tqdm import tqdm

def green(raw_data='sulige_0304/', out_data='NewData/', add_weight=0.3, light=20,ratio=30):
    '''

    :param raw_data: 原始数据路径
    :param out_data: 生成数据路径
    :param add_weight: 绿色前景比例 0-1之间 值越大绿色前景越浓
    :param light: 增亮 0-255之间 值越大画面越亮
    :param ratio: 图片画质 0-100 值越大画质越高。
    :return:
    '''
    shutil.copytree(raw_data, out_data, dirs_exist_ok=True)
    for img_p in tqdm(Path(out_data).rglob('*.jpg')):
        img = cv2.imread(str(img_p))
        mask = np.zeros_like(img)
        mask[np.sum(img,axis=2)>0]=[0,255,0]
        merged = cv2.addWeighted(img, 1-add_weight, mask, add_weight, light)
        # cv2.imshow('merged',merged)
        # cv2.waitKey(0)
        # b, g, r = cv2.split(img)
        # g[np.logical_and(g > 0, g < 255 - ADJUST)] += ADJUST
        # # g += ADJUST
        # r[r > 255-ADJUST-ADJUST] -= ADJUST
        # b[b > 255-ADJUST-ADJUST] -= ADJUST
        # merged = cv2.merge([b, g, r])
        # merged += light

        cv2.imwrite(str(img_p), merged,[cv2.IMWRITE_JPEG_QUALITY, ratio])
        # cv2.imshow('after', merged)
        # cv2.imshow('raw', img)
        # cv2.waitKey()
    print('task is end')
if __name__ == '__main__':
    green()