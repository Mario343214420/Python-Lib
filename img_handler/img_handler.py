import cv2
import os
s = os.walk(top='./imgs', topdown=True, onerror=None, followlinks=False)
arr = ['']
for curDir, dirs, files in s:
    for name in files:
        img = cv2.imread("./imgs/%s"%(name))
        h = img.shape[0]
        print(h)
        cropped = img[88:h-107, 276:998]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imwrite("./imgs/res-%s"%(name), cropped)