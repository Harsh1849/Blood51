import cv2
import numpy as np
from PIL import Image

saturation = 0
i=0

img = cv2.imread("1.jpg")

width,height,_ = img.shape

result = cv2.fastNlMeansDenoisingColored(img,None,20,10,7,21)

hsv_img = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
#cv2.imshow("HSV Image", hsv_img)

for x in range(width):
   for y in range(height):
      i=i+1
      saturation = saturation + hsv_img[x,y][0]

avg = saturation/i

lower_limit = np.array([avg-5, 0, 0])
upper_limit = np.array([avg+15, 255, 255])

print("lower limit : ",lower_limit)
print("upper limit : ",upper_limit)

cv2.waitKey(1)

