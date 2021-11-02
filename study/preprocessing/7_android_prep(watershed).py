# 안드로이드에서 받은 이미지 파일 처리 클래스

import cv2
import os
import numpy as np
import pytesseract
import re


#pytesseract.pytesseract.tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract.exe'

class prep:

    # 파일경로 설정
    def __init__(self, file_path,file_name):
        self.file_path = file_path  # 이미지 들어있는 파일경로
        self.file_names = os.listdir(file_path)  # 이미지 파일 이름
        self.src_name = file_name #sum([name.split('.')[:1] for name in self.file_names], [])[0]  # 이미지 파일이름
        self.src_file = self.file_path + '/' + self.src_name + '.jpg'

    # 이미지 전처리 후 저장 경로 생성
    def create_path(self, file_path):
        try:
            if not os.path.exists(self.file_path):
                os.makedirs(self.file_path)
        except OSError:
            print(f"{self.file_path}는 없는 경로입니다. 해당 이미지의 text_roi 폴더를 생성합니다.")


    # 안드로이드에서 전송한 이미지 파일 ROI 영역 탐지
    # return 딕셔너리 - key: 이미지 이름, value: 8-segment영역 정보 튜플 (x, y, w, h)
    def find_8seg(self):

        src_roi = dict()    # 좌표를 저장할 딕셔너리 생성
        src_file = '.'+self.file_path + '/' + self.src_name + '.jpg'
        print(f"- 수행파일:{src_file}")  # 확인

        # 좌표를 저장할 경로 생성
        roi_path = './static/img'  #+ self.src_name
        self.create_path(roi_path)
        print(f"- 저장경로:{roi_path}")


        ## 이미지 읽어오기 - GrayScale
        src = cv2.imread(self.src_file, cv2.IMREAD_GRAYSCALE)

        if src is None:
            print('Image load failed!')
            #sys.exit()


        ## Histogram equalization
        src = cv2.equalizeHist(src)


        ## Binary
        # parameter
        max_val = 255
        C = -10
        bin = 10    # block_size 홀수
        if (src.shape[1] // bin) % 2 == 0:
            block_size = src.shape[1] // bin + 1
        else:
            block_size = src.shape[1] // bin

        src = cv2.adaptiveThreshold(src, max_val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                           block_size, C)
        cv2.imwrite(roi_path + '/' + self.src_name + '_binary' + '.jpg', src)   # 저장


        ## contouring
        contours, hierarchy = cv2.findContours(src, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_TC89_L1)
        src_check = cv2.imread(self.src_file, cv2.IMREAD_COLOR)
        src_contour = cv2.drawContours(src_check, contours, contourIdx=-1, color=(0, 255, 0), thickness=4)
        cv2.imwrite(roi_path + '/' + self.src_name + '_contour' + '.jpg', src_contour)   # 저장


        # 추려낸 contours 대상으로 사각형 그리기
        data_roi_coo = set()   # 좌표 저장할 set
        serial_id = ""
        for con in contours:
            perimeter = cv2.arcLength(con, True)    # 외곽선 둘레 길이

            # x, y, w, h의 namespace 설정
            x = 0
            y = 0
            w = 0
            h = 0

            for epsilon in range(100, 200):
                epsilon = epsilon / 1000

                # 빠른 객체탐지를 위해 작은 값 무시
                if epsilon * perimeter < 20.0:
                    break

                # 외곽선 근사화하여 좌표 반환
                approx = cv2.approxPolyDP(con, epsilon * perimeter, True)

                # 4개의 코너를 가지는 Edge Contour에 대해 사각형 추출
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(con)        # 좌표를 감싸는 최소면적 사각형 정보 반환


                    src_w = src.shape[1]
                    src_h = src.shape[0]

                    # 8-segment ROI 특정
                    if (w < 0.15 * src_w) or (w > 0.6 * src_w) or (h > 0.2 * src_h) or \
                            (w / h > 3.5) or (w / h < 1.8) or \
                            (y + h > 0.85 * src_h) or (y < 0.1 * src_h) or (x + w > 0.85 * src_w) or (
                            x < 0.15 * src_w):
                        break

                    # ROI 좌표를 튜플로 저장함
                    data_roi_coo.add((x, y, w, h))

                    # 사각형 그리기
                    src_check = cv2.imread(self.src_file, cv2.IMREAD_COLOR)
                    rect = cv2.rectangle(src_check, (x, y), (x+w, y+h), (255, 0, 255), thickness=4)
                    # cv2.imwrite(roi_path + '/' + self.src_name + '_rect' + '.jpg', rect)  # 저장
                    # cv2.imshow('roi', rect)
                    # key = cv2.waitKey()
                    # if key == 27:
                    #     break

                    # 최소 사각형 추출
                    ((x1, y1), (w1, h1), angle) = cv2.minAreaRect(con)
                    if h1 > w1:
                        angle = angle - 90
                        h1, w1 = w1, h1
                    min_rect = ((x1, y1), (w1, h1), angle)
                    box = cv2.boxPoints(min_rect)
                    box = np.int0(box)
                    src_contour = cv2.drawContours(src_check, [box], 0, (0, 255, 0), 1)

                    # 이미지 회전
                    image_center = tuple(np.array(src_check.shape[1::-1]) / 2)
                    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
                    src_rot = cv2.warpAffine(src_check, rot_mat, src_check.shape[1::-1], flags=cv2.INTER_LINEAR,
                                            borderValue=(255, 255, 255))
                    cv2.imwrite(roi_path + '/' + self.src_name + '_rot' + '.jpg', src_rot)  # 저장

                    src_rot = cv2.cvtColor(src_rot, cv2.COLOR_BGR2GRAY)

                    # 이미지 투시변환 (사각형 두개 이용)
                    if h1 > w1:
                        h1, w1 = w1, h1

                    x1 = int(x1 - w1 * 0.5)
                    y1 = int(y1 - h1 * 0.5)
                    w1 = int(w1)
                    h1 = int(h1)
                    left_top = (int(x1), int(y1))
                    left_bot = (int(x1), int(y1 + h1))
                    right_top = (int(x1 + w1), int(y1))
                    right_bot = (int(x1 + w1), int(y1 + h1))

                    rows, cols = src_rot.shape[:2]
                    pts1 = np.float32([[0, 0], [0, rows], [cols, 0], [cols, rows]])
                    pts2 = np.float32([[0 + (x - left_top[0]) * 1, 0 + (y - left_top[1]) * 1],
                                       [0 + (x - left_bot[0]) * 1, rows + (y + h - left_bot[1]) * 1],
                                       [cols + (x + w - right_top[0]) * 1, 0 + (y - right_top[1]) * 1],
                                       [cols + (x + w - right_bot[0]) * 1, rows + (y + h - right_bot[1]) * 1]])

                    mtrx = cv2.getPerspectiveTransform(pts1, pts2)
                    dst = cv2.warpPerspective(src_rot, mtrx, (cols, rows))
                    # 투시변환 종료
                    # 회전 & 투시 변환 후 이진화
                    # img = cv2.adaptiveThreshold(dst, max_val, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                    #                             block_size, 15)

                    water_img = self.watershed(dst)

                    # OCR 수행
                    config = ('-l kor+eng --oem 1 --psm 3')
                    text = pytesseract.image_to_string(water_img, config=config)
                    print(text)
                    pat = re.compile('(\d{2})\W+(\d{2})\W+(\d{7})\W+(\d{4})')
                    mc = pat.findall(text)
                    if not mc:
                        break
                    else:
                        serial_id = ''.join(mc[0])
                        break

        src_roi[self.src_name] = data_roi_coo

        return src_roi, serial_id


    # ROI를 탐지하지 못한 경우의 처리
    def no_box(self):
        # 이미지 전처리 결과 딕셔너리 가져오기
        src_roi, serial_id = self.find_8seg()
        result_roi = 1

        print(f"-----------------------------ROI of {self.src_name}-----------------------------")

        if len(src_roi[self.src_name]) == 0 or len(serial_id) == 0:
            print("ROI를 탐지하지 못했습니다. 다시 촬영해주십시오.")
            result_roi = 0
        elif len(src_roi[self.src_name]) == 2 or len(serial_id) == 0:
            print("ROI가 2개 탐지하였습니다. 첫번째 ROI를 기준으로 OCR 수행합니다.")
            result_roi = 2
        else:
            print(src_roi[self.src_name])
            result_roi = 1

        return result_roi, serial_id

    def watershed(self, gray):
        """
        Performs a marker-based image segmentation using the watershed algorithm.
        :param src: 8-bit 1-channel image.
        :return: 32-bit single-channel image (map) of markers.
        """
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        # cv2.imwrite('{}.png'.format(np.random.randint(1000)), src)
        # gray = src.copy()
        # img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        # h, w = gray.shape[:2]
        # block_size = (min(h, w) // 4 + 1) * 2 + 1
        # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, 0)
        _ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        cv2.imshow('thresh', thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # noise 제거
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # 확실한 배경 찾기
        # 흰색 영역이 줄어듦
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        cv2.imshow('sure_bg', sure_bg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # 확실한 전경 찾기
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)
        # _ret, sure_fg = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, cv2.THRESH_BINARY)
        _ret, sure_fg = cv2.threshold(dist_transform, 0.8 * dist_transform.max(), 255, 0)

        cv2.imshow('sure_fg', sure_fg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # unknown : 배경에서 전경을 제외하여 확실하지 않은 영역 찾기
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        cv2.imshow('unknown', unknown)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Marker label
        lingret, marker_map = cv2.connectedComponents(sure_fg)
        # Add one to all labels so that sure background is not 0, but 1
        marker_map = marker_map + 1

        # Now, mark the region of unknown with zero
        marker_map[unknown == 255] = 0
        marker_map = cv2.watershed(img, marker_map)
        print(np.unique(marker_map))
        img[marker_map == -1] = [255, 0, 0]
        cv2.imshow('Watershed', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return img
