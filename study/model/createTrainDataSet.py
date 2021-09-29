import os,cv2,keras
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import csv

import CommonPreprocessing as common

ELECT_PATH = "/content/drive/MyDrive/Colab Notebooks/k-digital/00_lpinProject/data/ElectricityMeter"
COORDI_PATH = "/content/drive/MyDrive/Colab Notebooks/k-digital/00_lpinProject/data/roi"

# 전력량계량기 이미지로부터 전력량 세그먼트 영역을 찾는 모델
class FindSegmentArea :

    def __init__(self, elect_file_path, coordi_file_path):
        self.elect_file_path = elect_file_path
        self.coordi_file_path = coordi_file_path

    # IoU 계산하는 함수
    def get_iou(bb1, bb2):
        assert bb1['x1'] < bb1['x2']
        assert bb1['y1'] < bb1['y2']
        assert bb2['x1'] < bb2['x2']
        assert bb2['y1'] < bb2['y2']

        x_left = max(bb1['x1'], bb2['x1'])
        y_top = max(bb1['y1'], bb2['y1'])
        x_right = min(bb1['x2'], bb2['x2'])
        y_bottom = min(bb1['y2'], bb2['y2'])

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
        bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

        iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
        assert iou >= 0.0
        assert iou <= 1.0
        return iou

    # Selective Search Segmentation을 이용하여 IoU 계산하는 함수
    def searchSegmentation(self):
        # 사용할 search segmentation 의 수
        numUseRects = 150
        train_images = []
        train_labels = []

        # 모든 좌표파일 개수만큼 순회
        for e, i in enumerate(os.listdir(self.coordi_path)):
            try:
                # 이미지파일명 생성
                filename = i.split(".")[0] + ".jpg"
                # 이미지파일 읽어오기
                image = cv2.imread(os.path.join(self.elect_file_path, filename))
                # 사이즈 줄이기
                image = self.resize(image, 700)
                # 좌표를 저장할 dictionary
                gtvalue = dict()
                # 좌표파일 열기
                f = open(os.path.join(self.coordi_path, i), 'r', encoding='utf-8')
                # 파일내용 읽어오기
                rdr = csv.reader(f)
                # 내용 라인 수 만큼 순회(어차피 1줄)
                for line in rdr:
                    x1 = int(line[0])
                    y1 = int(line[1])
                    x2 = int(line[2])
                    y2 = int(line[3])

                    # 좌표저장
                    gtvalue = {"x1": x1, "x2": x2, "y1": y1, "y2": y2}

                # 초기화
                ss.setBaseImage(image)
                #  SelectiveSearch(저퀄리티 고속)
                ss.switchToSelectiveSearchFast()
                # 이미지파일에 대한 selective search segmentation 생성하여 저장
                ssresults = ss.process()
                # 출력할 이미지생성
                imout = image.copy()
                counter = 0
                falsecounter = 0
                flag = 0
                fflag = 0
                bflag = 0

                # 생성된 search segmentation의 수만큼 순회
                for e, result in enumerate(ssresults):
                    # 150개까지 생성
                    if e < numUseRects and flag == 0:
                        # search segmentation의 왼쪽 상단좌표와 width, height취득
                        x, y, w, h = result

                        # iou 추출
                        iou = self.get_iou(gtvalue, {"x1": x, "x2": x + w, "y1": y, "y2": y + h})
                        #
                        if counter < 30:
                            if iou > 0.70:
                                timage = imout[y:y + h, x:x + w]
                                resized = cv2.resize(timage, (224, 224), interpolation=cv2.INTER_AREA)
                                train_images.append(resized)
                                # 레이블 1 저장
                                train_labels.append(1)
                                counter += 1
                        else:
                            fflag = 1
                        if falsecounter < 30:
                            if iou < 0.3:
                                timage = imout[y:y + h, x:x + w]
                                resized = cv2.resize(timage, (224, 224), interpolation=cv2.INTER_AREA)
                                train_images.append(resized)
                                # 레이블 0 저장
                                train_labels.append(0)
                                falsecounter += 1
                        else:
                            bflag = 1
                    if fflag == 1 and bflag == 1:
                        print("inside")
                        flag = 1
            except Exception as e:
                print(e)
                print("error in " + filename)
                continue



if __name__ == '__main__':
    # If image path and f/q is not passed as command
    # line arguments, quit and display help message

    ELECT_FILE_PATH = "../data/ElectricityMeter"
    image_name = "01232010345_P1132.jpg"

    # speed-up using multithreads
    # 멀티스레드 속도높이기
    cv2.setUseOptimized(True);
    cv2.setNumThreads(4);
