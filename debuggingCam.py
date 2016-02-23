import cv2
import numpy as np

camera = cv2.VideoCapture(0)
print camera.isOpened()
(ass,frame) = camera.read()
cv2.imshow("test",frame)
