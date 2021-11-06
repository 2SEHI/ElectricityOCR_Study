# class화 하기
# pip install opencv-python==3.4.11.45
# pip install numpy
# pip install opencv-contrib-python==3.4.11.45
# pip install matplotlib
import os
import cv2
import csv
# from matplotlib import pyplot as plt
import numpy as np
from pytesseract import *

# 1. resize
# 2. 점을 4개 그리기
class ocr_text_area:
    # 왼쪽 상단 : (x1, y1), 오른쪽 상단 : (x2,y2), 왼쪽 하단 : (x3, y3), 오른쪽 하단:(x4, y4)
    def __init__(self, img_dir):
        self.img_dir = img_dir
        self.fileFullName = None
        self.filename = None
        self.textImg = None
        self.failed_img_list = []

        # 폴더 내의 모든 파일명 가져오기
        file_name_list = os.listdir(img_dir + 'textImage')
        file_name_list.sort(reverse=False)
        print('ROI 추출할 파일의 개수 : ', file_name_list)
        self.fileNameList = file_name_list

    def read_one_img(self):
        img_dir = self.img_dir + '/' + self.fileFullName
        # 파일명과 확장자 분리
        filename, ext = os.path.splitext(self.fileFullName)
        self.filename = filename

        print('[이미지 경로] ', img_dir)
        self.textImg = cv2.imread(img_dir)

    def read_several_img(self):
        total = len(self.fileNameList)
        print(f'<<<<<<<<<<<<<<<<<<<<<<<< {total}개 이미지의 OCR 시작 >>>>>>>>>>>>>>>>>>>>>>>>>>>')
        count = 1
        success_count = 0
        try:
            for fileFullName in self.fileNameList[:total]:
                print(f'[start] ------------------------ {fileFullName} OCR 시작 ------------------------')
                print(f'[{count}] : {fileFullName}')
                self.fileFullName = fileFullName

                self.read_one_img()
                serial_id = self.img_2_text()
                print('제조번호 : ' , serial_id)
                print(f'[end] ------------------------ {fileFullName} OCR 종료 ------------------------ ')
                print("\n")

        except Exception as e:
            print(e)
        finally:
            print(f'<<<<<<<<<<<<<<<<<<<<<<<< {success_count}개의 OCR 성공! >>>>>>>>>>>>>>>>>>>>>>>>>>>')

    def get_real_serial_id(self):
        with open(self.img_dir + '/real_serial_id.csv', newline='') as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader) :
                print(row)

    def img_2_text(self):
        text_img = self.textImg.copy()
        text = image_to_string(text_img, lang="eng",
                               config='--psm 7 -c preserve_interword_spaces=1')
        save_dir = self.img_dir + '/text/serial_id.csv'
        wf = open(save_dir, 'a')
        wf.write(self.filename + ',')
        wf.write('\n')
        wf.close()
        return text

if __name__ == "__main__":
    ROOT_DIR = '../../data/'
    ORIGINAL_DIR = '/original/G-Type2'

    ocrClass = ocr_text_area(ROOT_DIR)
    ocrClass.read_several_img()
