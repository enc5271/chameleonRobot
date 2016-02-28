import cv2
import numpy as np

camera = cv2.VideoCapture('/dev/video0')
print camera.isOpened()
camera.open('/dev/video0')
ass,frame = camera.read()
#frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
print ass
cv2.imshow('IT WORKS',cv2.imdecode(frame))
camera.release()
cv2.destroyAllWindows()