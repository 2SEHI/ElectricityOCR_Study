import cv2


class commonProcess:
    def __init__(self, img_dir, img_name):
        self.img_dir = img_dir
        self.img_name = img_name

    # 이미지 크기(w, h)를 (500,h*(500/w))의 비율로 정형화하기
    def resize(self, img, width):
        # 이미지의 width 가 500보다 클 경우 width 에 맞춰서 축소, 확대
        # 나중에 원하는 width로 수정하고 **변수지정** 하기
        ratio = width / img.shape[1]
        dim = (width, int(img.shape[0] * ratio))
        # 이미지 확대 : cv2.INTER_CUBIC, cv2.INTER_LINEAR
        # 이미지 축소 : cv2.INTER_AREA
        # dstSize:절대크기. (너비, 높이)
        # fx, fy : 상대 크기
        resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        # 크기를 조정한 이미지를  resized 폴더에 저장
        cv2.imwrite(self.img_dir + '/resized/' + self.img_name + '.jpg', resized_img)

        return resized_img
