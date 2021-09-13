import cv2
import numpy as np
from pytesseract import *
import re
import matplotlib.pyplot as plt

class MatchTemplate:
    def __init__(self):
        pass

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
        return resized_img

    # 직사각형 형태의 ROI추출하는 함수
    def selectROI(self, img):
        x,y,w,h = cv2.selectROI('img',img,False, False)
        print(x,y,w,h)

        roi = None
        if w and h :
            templ_roi = img[y:y+int(w * 0.5), x:x+w]
            cv2.imshow('cropped', templ_roi)
            # cv2.imwrite(IMAGE_DIR + 'G-Type_area.jpg', templ_roi)
            cv2.moveWindow('cropped', 0,0)

        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return templ_roi


    # 문자영역에 대한 이미지 전처리
    # otsuThreshold 이진화 -> 팽창,침식 -> close
    def preprocessing(self, img):
        img_copy = img.copy()
        # TODO otsu Threshold
        ret3, otsu_img = cv2.threshold(img_copy,  0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # TODO 팽창,침식
        # 모폴로지 구조 요소(커널) 생성 함수
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # erode : 침식, dilate : 팽창
        # iterations: Erosion 반복 횟수
        # dilate = cv2.dilate(otsu_img, kernel, iterations=1)
        # erode = cv2.erode(otsu_img, kernel, iterations=1)

        # MORPH_GRADIENT : dilate와 erode를 같이 해줌
        gradient = cv2.morphologyEx(otsu_img, cv2.MORPH_GRADIENT, kernel)

        # TODO close로 문자들 뭉치기
        c_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
        close = cv2.morphologyEx(gradient, cv2.MORPH_CLOSE, c_kernel)

        cv2.imshow("close", close)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return close

    # contouring
    def contouring(self, image, src_gray):
        # 이미지 색 반전
        binary = cv2.bitwise_not(image)
        contours , hierachy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        src_copy = src_gray.copy()
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            area = cv2.contourArea(contour=contour)
            
            # 외곽선 크기가 너무 작으면 무시
            # TODO 공통값 찾기
            if area < 50:
                continue

            # 사각형 그리기
            cv2.rectangle(src_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow("contour", src_copy)
        # cv2.imwrite(IMAGE_DIR + "60_K-Digital_Training_Project_6contour.jpg", src_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 선택한 Type영역과 매칭하는 영역찾기
    def getTextArea(self, templ, src):
        
        # G-Type 표시 영역 찾기
        # TM_CCORR_NORMED : 정규화된 상관관계 방법(TM_CCORR_NORMED) 밝은곳이 매칭지점
        result = cv2.matchTemplate(resized_src, templ, cv2.TM_CCORR_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

        # G-Type영역의 x,y,w,h 저장
        x, y = maxLoc[0], maxLoc[1]
        w, h = templ.shape[:2]
        # G type영역의 사각형 그리기
        cv2.rectangle(resized_src, maxLoc, (maxLoc[0]+ h, maxLoc[1] + w), (255, 0, 0), 2)

        # G-Type영역크기를 이용하여 문자영역을 저장
        ob_x, ob_y = (x-int(h * 1.2), y)
        ob_w, ob_h = (int(w * 9.43), int(h * 6.5))
        # 문자 추출대상 영역 그리기
        cv2.rectangle(resized_src, (ob_x, ob_y), (ob_x + ob_h, ob_y + ob_w), (255, 0, 0), 2)

        # 문자영역
        textarea = src[ob_y:ob_y + ob_w, ob_x:ob_x + ob_h]
        
        # templ과 문자 추출 대상 영역 띄우기
        cv2.imshow("textarea", textarea)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # tesseract 문자 인식
        # text = image_to_string(textarea, lang="kor+eng",
        #                        config='--psm 1 -c preserve_intertword_spaces=1')
        # print(text)

        return textarea

# 원본 이미지경로
IMAGE_DIR = '../image_sample/'
# 읽어올 원본 이미지 파일 이름
src_image_name = 'image00003'

# 매칭할 이미지 경로
MATCH_IMAGE_DIR = '../match_image/'

# 매칭 이미지 파일 이름
match_image_name = 'G-Type_type-name2'
# resize할 width의 크기
WIDTH = 700

if __name__ == "__main__":
    matchTemplate = MatchTemplate()

    # gray scale한 이미지
    src_gray = cv2.imread(IMAGE_DIR + src_image_name + '.jpg', cv2.IMREAD_GRAYSCALE)

    # 이미지 resize
    resized_src = matchTemplate.resize(src_gray)

    # "G-type"을 추출
    templ = matchTemplate.selectROI(resized_src)

    src_copy = resized_src.copy()

    if templ is not None :
        # 문자영역의 이미지 가져오기
        textarea = matchTemplate.getTextArea(templ, resized_src)
        
        # 문자영역이미지 전처리
        pre_img = matchTemplate.preprocessing(textarea)

        # 문자영역 contouring
        matchTemplate.contouring(pre_img, textarea)