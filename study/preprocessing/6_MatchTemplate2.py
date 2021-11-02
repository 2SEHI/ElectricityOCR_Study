import cv2
import numpy as np
import sys
# image template_path
# :01:04 ▓▒░─╮
# python study/preprocessing/6_MatchTemplate2.py data/image_sample/match_image.jpg data/image_sample/ElectricityMeter/847207D64B0D_P1179.jpg
if len(sys.argv) < 3:
    print('Usage: python match.py <template.png> <image.png>')
    sys.exit()

template_path = sys.argv[1]
# print(template_path)

template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
channels = cv2.split(template)
print('channels : ',channels)
zero_channel = np.zeros_like(channels[0])
# mask 생성
mask = np.array(channels[0])
# 전력량계 image 읽어오기
image_path = sys.argv[2]
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(len(channels))
mask[channels[3] == 0] = 1
mask[channels[3] == 100] = 0

# transparent_mask = None
# According to http://www.devsplanet.com/question/35658323, we can only use
# cv2.TM_SQDIFF or cv2.TM_CCORR_NORMED
# All methods can be seen here:
# http://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching/template_matching.html#which-are-the-matching-methods-available-in-opencv
method = cv2.TM_SQDIFF  # R(x,y) = \sum _{x',y'} (T(x',y')-I(x+x',y+y'))^2 (essentially, sum of squared differences)

transparent_mask = cv2.merge([zero_channel, zero_channel, zero_channel, mask])
result = cv2.matchTemplate(image, template, method, mask=transparent_mask)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print('Lowest squared difference WITH mask', min_val)

# Now we'll try it without the mask (should give a much larger error)
transparent_mask = None
result = cv2.matchTemplate(image, template, method, mask=transparent_mask)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print('Lowest squared difference WITHOUT mask', min_val)