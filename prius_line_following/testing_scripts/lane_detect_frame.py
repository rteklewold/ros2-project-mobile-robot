import cv2
import numpy as np

image = cv2.imread('/home/ecn/output.png')
print(image.shape)
light_line = np.array([100, 100, 100])
dark_line = np.array([200, 200, 200])
print(image[220,300,:])
mask = cv2.inRange(image, light_line, dark_line)

mask_edge = cv2.Canny(mask, 10, 40)
cv2.imshow('mask edge', mask_edge)
cv2.waitKey(0)