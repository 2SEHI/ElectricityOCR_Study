import cv2
import numpy as np

# 공통 전처리
class CommonPreprocessing:
    def __init__(self):
        pass

    # 이미지 크기(w, h)를 (width,h*(width/비율))로 정형화하기
    def resize(img, width):
        src_height, src_width = img.shape[:2]
        # 이미지의 width가 500보다 클 경우 width에 맞춰서 축소, 확대
        # TODO 나중에 원하는 width로 수정하고 **변수지정** 하기
        ratio = width / src_width
        src_height, src_width = int(src_height * ratio), int(src_width * ratio)

        # 이미지 확대 : cv2.INTER_CUBIC, cv2.INTER_LINEAR
        # 이미지 축소 : cv2.INTER_AREA
        # dstSize:절대크기. (너비, 높이)
        # fx,fy : 상대 크기
        resized_img = cv2.resize(img, (src_width, src_height))
        # 영상을 화면에 출력
        return resized_img

    # 직사각형 형태의 ROI추출하는 함수
    def crop_select_ROI(self, img):
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

    # 좌표를 정렬
    # perspective_transform에서 호출함
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
    
    # 투시변환
    # image : 투시변환할 이미지
    # pts : x,y좌표 4개의 list
    def perspective_transform(self, image, pts):
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
        warped = cv2.warpPerspective(image, M, (int(maxWidth), int(maxHeight)))

        return warped
    
    # 이미지를 화면에 출력하는 함수
    def imshow(self, imageName, image):
        cv2.imshow(imageName, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()