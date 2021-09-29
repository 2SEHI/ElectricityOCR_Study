import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt6Opencv


# Calculate skew angle of an image
def getSkewAngle(cvImage) -> float:
    # 이미지 복사
    newImage = cvImage.copy()
    
    # 가우시안필터를 이용하여 잡음제거
    blur = cv2.GaussianBlur(newImage, (5, 5), 0)

    # 모폴로지 구조 요소(커널) 생성 함수
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    # dilate : 이미지 팽창
    dilate = cv2.dilate(blur, kernel, iterations=3)

    # otsu : 이미지 이진화
    thresh = cv2.threshold(dilate, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # 케니 에지 검출
    # 약한 에지 픽셀이 강한 에지 픽셀과 서로 연결되어 있다면 에지로 판단
    canny_img = cv2.Canny(thresh, 100, 250, apertureSize=3)

    cv2.imshow('canny_img', canny_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # 확률적 허프 선 변환 : 무작위로 선정한 픽셀에 대해 허프 변환을 수행
    # 엣지를 강하게 하고 threshold를 낮게 지정해주어야 합니다.
    # lines = cv2.HoughLinesP(img, rho, theta, threshold, lines, minLineLength, maxLineGap)
    # rho: pixcel단위
    # minLineLength(optional): 선으로 인정할 최소 길이
    # maxLineGap(optional): 선으로 판단할 최대 간격
    # lines: 검출된 선 좌표, N x 1 x 4 배열 (x1, y1, x2, y2)
    # 이외의 파라미터는 cv2.HoughLines()와 동일
    lines = cv2.HoughLinesP(canny_img, 1, np.pi/180, 10, None, 30, 2)
    for line in lines:
        # 검출된 선 그리기 ---③
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

    merged = np.hstack((img, canny_img))
    cv2.imshow('Probability hough line', merged)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Find largest contour and surround in min area box
    # 가장 큰 컨투어 저장
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle


    def contouring(self, image):

        contours , hierachy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            area = cv2.contourArea(contour=contour)
            # 외곽선 크기가 너무 작으면 무시
            if area < 10000:
                continue
            approx = cv2.approxPolyDP(contour,cv2.arcLength(contour, True)*0.02, True)
            vtc = len(approx)
            print(vtc)
            if vtc == 4:
                self.setLabel(image, contour, 'object')

        cv2.imshow("contour_image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

IMAGE_DIR = '../images/'
BLUE_COLOR = (255,0,0)
GREEN_COLOR = (0,255,0)
RED_COLOR = (0,0,255)
image_name = 'e-type_sample'

img = cv2.imread(IMAGE_DIR + image_name + '.jpg', cv2.IMREAD_GRAYSCALE)

rotateImage=deskew(img)

cv2.imshow('rotateImage', rotateImage)
cv2.waitKey()
cv2.destroyAllWindows()