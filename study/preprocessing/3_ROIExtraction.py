# class화 하기
# pip install opencv-python==3.4.11.45
# pip install numpy
# pip install opencv-contrib-python==3.4.11.45
# pip install matplotlib
import os
import cv2
# from matplotlib import pyplot as plt
import numpy as np
from pytesseract import *

# 1. resize
# 2. 점을 4개 그리기
class extract_roi_class:
    # 왼쪽 상단 : (x1, y1), 오른쪽 상단 : (x2,y2), 왼쪽 하단 : (x3, y3), 오른쪽 하단:(x4, y4)
    def __init__(self, img_dir, numOfFile, fileFullName=None):
        self.img_dir = img_dir
        self.fileFullName = None
        self.fileNameList = None
        self.filename = None
        self.originImg = None
        self.failed_img_list = []

        # 1개의 파일
        if numOfFile == 1:
            self.fileFullName = fileFullName
            print('1개의 파일에서 ROI 추출 : ', self.fileFullName)

        # 2개 이상의 파일
        else:

            # 폴더 내의 모든 파일명 가져오기
            fileNameList = os.listdir(img_dir + ORIGINAL_DIR)
            fileNameList.sort(reverse=False)
            print('ROI 추출할 파일의 개수 : ', fileNameList)
            self.fileNameList = fileNameList

    def read_one_img(self):
        img_dir = self.img_dir + ORIGINAL_DIR + '/' + self.fileFullName

        # 파일명과 확장자 분리
        filename, ext = os.path.splitext(self.fileFullName)
        self.filename = filename

        print('[이미지 경로] ', img_dir)
        self.originImg = cv2.imread(img_dir)
        # cv2.imshow('original', self.originImg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def extract_several_roi(self, num):
        total = len(self.fileNameList)
        print(f'<<<<<<<<<<<<<<<<<<<<<<<< {total}개 이미지의 ROI 추출 시작 >>>>>>>>>>>>>>>>>>>>>>>>>>>')
        if num > 0:
            total = num
        count = 1
        success_count = 0
        try:
            for fileFullName in self.fileNameList[:total]:
                print(f'[start] ------------------------ {fileFullName} roi 추출 시작 ------------------------')
                print(f'[{count}] : {fileFullName}')
                self.fileFullName = fileFullName

                self.read_one_img()
                roi_result = self.extract_roi()
                if roi_result:
                    success_count += 1
                print(f'[end] ------------------------ {fileFullName} roi 추출 종료 ------------------------ ')
                print("\n")

        except Exception as e:
            print(e)
        finally:
            print('실패 파일 목록 : ',self.failed_img_list)
            print(f'<<<<<<<<<<<<<<<<<<<<<<<< {success_count}개의 ROI 추출 성공! >>>>>>>>>>>>>>>>>>>>>>>>>>>')

    # 직사각형 형태의 ROI 추출하는 함수
    def extract_roi(self):
        print('[start] ROI 추출 시작', self.fileFullName)
        img = self.originImg.copy()

        x, y, w, h = cv2.selectROI(img)
        roi = img[y:y + h, x:x + w]

        roi_result = False
        if len(roi) > 0:
            # ROI를 화면에 보여줌
            cv2.imshow(self.filename + '_roi', roi)
            key = cv2.waitKey(0)
            # a를 누르면 roi 를 재추출하도록 roi 배열을 비움
            if key == ord('r'):
                roi = []
            cv2.destroyWindow(self.filename + '_roi')

        if len(roi) <= 0:
            # ROI 추출 실패한 이미지 파일명을 csv파일에 저장
            failed_roi_dir = self.img_dir + '/failedImageList.csv'

            print('roi 추출 실패한 이미지 파일명 저장 : ', failed_roi_dir)
            wf = open(failed_roi_dir, 'a')
            wf.write(self.fileFullName)
            wf.write('\n')
            wf.close()

            self.failed_img_list.append(self.fileFullName)
            print('[warning] 추출된 ROI 가 없습니다')
            print('[end] ROI 추출 실패!', self.fileFullName, end='\n')
        else :
            roi_result = True
            save_dir = self.img_dir + '/textImage/' + self.filename + '_text.jpg'
            print('[ROI 저장위치] ', save_dir)
            cv2.imwrite(save_dir, roi)
            print('[end] ROI 저장 성공!', self.filename + '_text.jpg', end='\n')

        return roi_result

    def read_several_img(self, num):
        total = len(self.fileNameList)
        print(f'<<<<<<<<<<<<<<<<<<<<<<<< {total}개 이미지의 ROI 추출 시작 >>>>>>>>>>>>>>>>>>>>>>>>>>>')
        if num > 0:
            total = num
        count = 1
        success_count = 0
        try:
            for fileFullName in self.fileNameList[:total]:
                print(f'[start] ------------------------ {fileFullName} roi 추출 시작 ------------------------')
                print(f'[{count}] : {fileFullName}')
                self.fileFullName = fileFullName

                self.read_one_img()
                roi_result = self.extract_roi()
                count += 1
                if roi_result:
                    success_count += 1
                print(f'[end] ------------------------ {fileFullName} roi 추출 종료 ------------------------ ')
                print("\n")

        except Exception as e:
            print(e)
        finally:
            print('실패 파일 목록 : ', self.failed_img_list)
            print(f'<<<<<<<<<<<<<<<<<<<<<<<< {success_count}개의 ROI 추출 성공! >>>>>>>>>>>>>>>>>>>>>>>>>>>')

    def img_2_text(self, img):
        text = image_to_string(img, lang="eng",
                               config='--psm 7 -c preserve_interword_spaces=1')
        print(text)
        return text

if __name__ == "__main__":
    ROOT_DIR = '../../data'
    ORIGINAL_DIR = '/original/G-Type2'

    # 1개의 파일에서 ROI추출
    FILE1 = 1
    # 2개 이상의 파일에서 ROI추출
    FILE2 = 2
    # roi 추출할 파일의 갯수
    # 0 : 폴더 내의 파일 전부
    number = 50

    readType = FILE1

    if readType == FILE1:
        filefullname = '01232004307_P148.jpg'
        roiClass = extract_roi_class(ROOT_DIR, FILE1, filefullname)
        roiClass.read_one_img()
        roiClass.extract_roi()
    elif readType == FILE2:
        roiClass = extract_roi_class(ROOT_DIR, FILE2)
        roiClass.extract_several_roi(number)
