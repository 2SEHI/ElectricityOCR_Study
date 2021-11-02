import sys, os
from model.OCRModel import OCRModel

# 상위 경로(Project/)를 system PATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    ocrModel = OCRModel()
    #
    #file_list = os.listdir('../static/img')
    #for filename in file_list[:1]:
    #    result_roi, sava_images, serial_cd = ocrModel.get_roi_images('../static/img', filename)
    filename = "01232009862_P181.jpg"
    result_roi, sava_images, serial_cd = ocrModel.get_roi_images('../static/img', filename)