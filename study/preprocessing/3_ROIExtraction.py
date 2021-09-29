import cv2
import numpy as np

IMAGE_DIR = '../image_sample/'
src_image_name = 'image00001'

WIDTH = 300

# 전력량계량기를 추출하기 위해서 문자영역을 뭉치게 만들어서 contouring함
# 문자영역이 잘 안뭉쳐짐
class OCRDetect:
    def __init__(self, src):
        # resize한 원본 컬러 사진
        self.src = self.resize(src)
        # resize한 원본 grayscale 사진
        self.src_gray = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)

    def findObject(self):
        src_gray_copy = self.src_gray.copy()
        src_copy = self.src.copy()

        C = 2
        # block size 와 감산값 설정
        b_size_fun = lambda x : x-1 if x % 2 == 0 else x
        height= src_gray_copy.shape[1]
        block_size = int(b_size_fun(height))
        # block_size = 11

        # TODO 임계치(Adaptive Threshold) :  영역을 분할하고 임계값을 자동으로 조정해 얻은 흑백 이미지
        # 입력 이미지, 최댓값, 적응형 이진화 플래그, 임곗값 형식, 블록 크기, 감산값
        # 적응형 이진화 플래그 : ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        # 임곗값 형식 : THRESH_BINARY, THRESH_BINARY_INV
        # 블록 크기 : 임계값 사용시 사용하는 브록 크기.3보다 같거나 큰 홀수를 지정
        # 감산값 : 블록 평균에서 감산값을 뺀 값을 임계값으로 사용
        adaptiveThreshold = cv2.adaptiveThreshold(src_gray_copy, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)


        # TODO 팽창 -> close로 문자들을 뭉치기
        # 모폴로지 구조 요소(커널) 생성 함수
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        # erode : 침식, dilate : 팽창
        # iterations: Erosion 반복 횟수
        dilate = cv2.dilate(adaptiveThreshold, kernel, iterations=1)
        erode = cv2.erode(adaptiveThreshold, kernel, iterations=1)
        close = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, kernel)


        # TODO HoughLinesP
        edges = cv2.Canny(close, 50, 150, apertureSize=3)
        threshold = 100  # 선 추출 정확도
        minLength = 100  # 추출할 선의 길이
        lineGap = 5  # 5픽셀 이내로 겹치는 선은 제외
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold, None, minLength, lineGap)

        gray = cv2.cvtColor(src_copy, cv2.COLOR_BGR2GRAY)
        for line in lines:
            # 검출된 선 그리기
            x1, y1, x2, y2 = line[0]
            cv2.line(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)


        


        # cv2.imshow("adaptiveThreshold", adaptiveThreshold)
        # cv2.imshow("dilate", dilate)
        # cv2.imshow("erode", erode)
        # cv2.imshow("close", close)
        cv2.imshow("HoughLinesP", gray)
        # TODO contouring

        self.contouring(gray)
        self.contouring2(gray)

        # cv2.imwrite(IMAGE_DIR + '60_K-Digital_Training_Project_1adaptiveThreshold.jpg', adaptiveThreshold)
        # cv2.imwrite(IMAGE_DIR + '60_K-Digital_Training_Project_2dilate.jpg', dilate)
        # cv2.imwrite(IMAGE_DIR + '60_K-Digital_Training_Project_3erode.jpg', erode)
        # cv2.imwrite(IMAGE_DIR + '60_K-Digital_Training_Project_4close.jpg', close)
        # cv2.imwrite(IMAGE_DIR + "60_K-Digital_Training_Project_5HoughLinesP.jpg", src_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def contouring(self, image):
        # 이미지 색 반전
        binary = cv2.bitwise_not(image)
        contours , hierachy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        src_copy = self.src.copy()
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            area = cv2.contourArea(contour=contour)
            # 외곽선 크기가 너무 작으면 무시
            if area < 1000:
                continue
            cv2.rectangle(src_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("contour", src_copy)
        # cv2.imwrite(IMAGE_DIR + "60_K-Digital_Training_Project_6contour.jpg", src_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def contouring2(self, img):
        # 이미지 색 반전
        img = cv2.bitwise_not(img)
        img_copy = self.src
        img2 = img_copy.copy()
        ret, imthres = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        # 가장 바깥 컨투어만 수집   --- ①
        contour, hierarchy = cv2.findContours(imthres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # 컨투어 갯수와 계층 트리 출력 --- ②
        print(len(contour), hierarchy)

        # 모든 컨투어를 트리 계층 으로 수집 ---③
        contour2, hierarchy = cv2.findContours(imthres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 컨투어 갯수와 계층 트리 출력 ---④
        print(len(contour2), hierarchy)

        # 가장 바깥 컨투어만 그리기 ---⑤
        cv2.drawContours(img_copy, contour, -1, (0, 255, 0), 3)
        # 모든 컨투어 그리기 ---⑥
        for idx, cont in enumerate(contour2):
            # 랜덤한 컬러 추출 ---⑦
            color = [int(i) for i in np.random.randint(0, 255, 3)]
            # 컨투어 인덱스 마다 랜덤한 색상으로 그리기 ---⑧
            cv2.drawContours(img2, contour2, idx, color, 3)
            # 컨투어 첫 좌표에 인덱스 숫자 표시 ---⑨
            cv2.putText(img2, str(idx), tuple(cont[0][0]), cv2.FONT_HERSHEY_PLAIN, \
                        1, (0, 0, 255))

        # 화면 출력
        cv2.imshow('RETR_EXTERNAL', img_copy)
        cv2.imshow('RETR_TREE', img2)
        # cv2.imwrite(IMAGE_DIR + "60_K-Digital_Training_Project_7RETR_EXTERNAL.jpg", img_copy)
        # cv2.imwrite(IMAGE_DIR + "60_K-Digital_Training_Project_8RETR_TREE.jpg", img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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
        return resized_img

if __name__ == "__main__":
    # 원본
    src = cv2.imread(IMAGE_DIR + src_image_name + '.jpg')

    # 원본을 GRAYSCALE로 변환
    src_gray = cv2.imread(IMAGE_DIR + src_image_name + '.jpg', cv2.IMREAD_GRAYSCALE)
    ocrdetect = OCRDetect(src)
    ocrdetect.findObject()
