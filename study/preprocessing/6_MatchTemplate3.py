# -*- coding: utf-8 -*-
import sys
print(sys.version)
import cv2
import numpy as np
# from pytesseract import
import re

class MatchTemplate:
    pass
    def match_templ(self):
        pass

# 원본 이미지경로
IMAGE_DIR = '../../data/image_sample/ElectricityMeter/'
# 원본 이미지경로
TEMPL_DIR = '../../data/image_sample/match_image.jpg'

# 읽어올 원본 이미지 파일 이름
src_image_name = '847207D64B50_P1145.jpg'

if __name__ == "__main__":
    matchTemplate = MatchTemplate()
    # 원본 이미지
    img_rgb = cv2.imread(IMAGE_DIR + src_image_name)

    # 원본 이미지를 GrayScale로 변경
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # 템플릿 이미지
    templ_color = cv2.imread(TEMPL_DIR, 0)
    w, h = templ_color.shape[::-1]

    # 결과 이미지
    dst = cv2.imread(IMAGE_DIR + src_image_name)

    # 유사도 결과
    res = cv2.matchTemplate(img_gray, templ_color, cv2.TM_CCOEFF_NORMED)
    print(res)
    threshold = 0.45
    loc = np.where(res > threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(dst, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    cv2.imshow("dst", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()