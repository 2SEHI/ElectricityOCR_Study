# class화 하기
# pip install opencv-python==3.4.11.45
# pip install numpy
# pip install opencv-contrib-python==3.4.11.45
# pip install matplotlib

import cv2
from matplotlib import pyplot as plt
import numpy as np
from pytesseract import *
# 1. resize
# 2. 점을 4개 그리기
class draw_coordinate:
    # 왼쪽 상단 : (x1, y1), 오른쪽 상단 : (x2,y2), 왼쪽 하단 : (x3, y3), 오른쪽 하단:(x4, y4)
    def __init__(self):
        self.xy_list = []

        self.count = 0
        self.click = False # Mouse 클릭상태. True:Click
        self.image = None

    # 마우스 이벤트처리에 의한 좌표 저장함수 호출
    # 이벤트, x,y좌표,
    def draw_point(self, event, x, y, flags, param):
        # 마우스 click : 1
        # 마우스를 누를 때마다 좌표 저장
        if event == cv2.EVENT_LBUTTONDOWN: # 마우스를 누른 상태
            # print(str(x),str(y))
            self.count += 1
            # 점찍기
            cv2.circle(self.image, (x, y), 10, (0, 255, 0), -1)
            # 그려진 좌표 저장
            self.xy_list.append([x,y])

            points1 = np.array(self.xy_list)
            # print(points1)
            # cv2.polylines(self.image, [points1], False, (255, 0, 0), 2)

    # 주요객체를 선택하여 주요객체의 좌표와 이미지를 저장하는 함수
    def save_coordinate(self, origin_img, image_name):

        self.image = origin_img.copy()
        cv2.namedWindow(image_name)
        # 마우스 이벤트처리에 의한 좌표 저장함수 호출
        cv2.setMouseCallback(image_name, self.draw_point)

        # main문 : 키보드로 esc를 받을때까지 화면을 계속 보여준다.
        while self.count < 4:
            cv2.imshow(image_name, self.image)  # 화면을 보여준다.
            k = cv2.waitKey(1) & 0xFF  # 키보드 입력값을 받고

            if k == 27:  # esc를 누르면 종료
                break

        # 주요객체 좌표를 그린 이미지 저장
        coordinate = self.init_points(self.xy_list)

        cv2.destroyAllWindows()
        return coordinate

    # 투시변환
    def init_points(self, pts):
        rect = self.sort_points(pts)
        (topLeft, topRight, bottomRight, bottomLeft) = rect

        w1 = abs(bottomRight[0] - bottomLeft[0])
        w2 = abs(topRight[0] - topLeft[0])
        h1 = abs(topRight[1] - bottomRight[1])
        h2 = abs(topLeft[1] - bottomLeft[1])

        # 최대 너비와 최대 높이를 계산
        maxWidth = max([w1, w2])
        maxHeight = max([h1, h2])

        dst = np.float32([[0, 0], [maxWidth-1, 0], [maxWidth-1, maxHeight-1], [0, maxHeight-1]])
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(self.image, M, (int(maxWidth), int(maxHeight)))



        # result = self.preprocessing2(dst)
        cv2.imwrite(IMAGE_DIR + '59_K-Digital_Training_Project_2.jpg', warped)
        cv2.imshow('warped', warped)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return warped

    # 좌표를 정렬
    def sort_points(self, pts):
        pts_copy = np.array(pts)

        rect = np.zeros((4,2), dtype="float32")

        s = pts_copy.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts_copy, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    # 이미지 크기(w, h)를 (500,h*(500/w))의 비율로 정형화하기
    def resize(self, img):
        # 이미지의 width가 500보다 클 경우 width에 맞춰서 축소, 확대
        # TODO 나중에 원하는 width로 수정하고 **변수지정** 하기
        ratio = WIDTH / img.shape[1]
        dim = (WIDTH, int(img.shape[0] * ratio))
        # 이미지 확대 : cv2.INTER_CUBIC, cv2.INTER_LINEAR
        # 이미지 축소 : cv2.INTER_AREA
        # dstSize:절대크기. (너비, 높이)
        # fx,fy : 상대 크기
        resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        # 영상을 화면에 출력
        # self.imshow(img, resized_img)
        cv2.imwrite(IMAGE_DIR + '59_K-Digital_Training_Project_1.jpg', resized_img)
        return resized_img


    def preprocessing(self, origin_img):
        # 이미지 복사
        copy_img = origin_img.copy()

        sharpening_1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

        #  sharpening
        dst = cv2.filter2D(copy_img, -1, sharpening_1)
        cv2.imwrite(IMAGE_DIR + '59_K-Digital_Training_Project_3.jpg', dst)
        cv2.imshow('Sharpening1', dst)

        # 가우시안필터를 이용하여 잡음제거
        # blur = cv2.GaussianBlur(copy_img, (5, 5), 0)
        adt = cv2.adaptiveThreshold(dst,maxValue=255.0,
                                adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                thresholdType=cv2.THRESH_BINARY_INV,
                                blockSize=19,
                                C=9
                            )
        cv2.imshow('adt_img', adt)
        # 모폴로지 구조 요소(커널) 생성 함수
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        # dilate : 이미지 팽창
        dilate = cv2.dilate(adt, kernel, iterations=1)
        # otsu : 이미지 이진화
        thresh = cv2.threshold(dilate , 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # self.contouring(self, thresh)
        # cv2.imshow('dilate', thresh)


        cv2.imshow('origin_img', thresh)
        cv2.imshow('dilate', dilate)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return thresh

    # 직사각형 형태의 ROI추출하는 함수
    def selectROI(self, img):
        x,y,w,h = cv2.selectROI('img',img,False, False)
        if w and h :
            roi = img[y:y+h, x:x+w]
            cv2.imshow('cropped', roi)
            cv2.moveWindow('cropped', 0,0)

        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def tesseract(self, img):
        text = image_to_string(img, lang="kor+eng",
                               config='--psm 1 -c preserve_intertword_spaces=1')
        return text

if __name__ == "__main__":

    IMAGE_DIR = '../image_sample/'
    image_name = 'image00009'
    WIDTH = 500
    # 흑백으로 영상읽기
    origin_img = cv2.imread(IMAGE_DIR + image_name + '.jpg', cv2.IMREAD_GRAYSCALE)

    # 주요객체 추출 클래스생성
    draw_coordinate = draw_coordinate()
    # 이미지 사이즈 조정
    resized_img = draw_coordinate.resize(origin_img)
    # selectROI = draw_coordinate.selectROI(resized_img)
    # 주요 객체의 좌표를 그리고 이미지와 좌표를 저장 -> 투시변환
    main_object = draw_coordinate.save_coordinate(resized_img, image_name)
    draw_coordinate.preprocessing(main_object)
    text = draw_coordinate.tesseract(main_object)
    print(text)

