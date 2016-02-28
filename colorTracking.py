import cv2
import numpy as np


def trackGreenTarget():
    cap = cv2.VideoCapture(0)
    #print cap.isOpened()
    if not cap.isOpened():
        print "Error Establishing Video Feed!"
        

    #PS2 Eye cam img: height = 480, width 640, channels = 3
    HEIGHT = 480
    WIDTH = 640
    BLUR_SIZE = 20

    #while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of GREEN color in HSV

    #Used the hsv value that young-ho gave but now it doesnt see anything
    lower_blue = np.array([40,120,90]) 
    upper_blue = np.array([70,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.blur(mask, (BLUR_SIZE,BLUR_SIZE))
    moments = cv2.moments(mask,0)
    area = moments['m00']
    #print area
    overlay = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    if(area > 150000):
    	x = moments['m10']/area
    	y = moments['m01']/area
    	print x, y
    	cv2.circle(overlay, (int(x), int(y)), 2, (255, 255, 255), 20)
        return (int(x),int(y))


        #frame = cv2.add(frame, overlay)
        #add the thresholded image back to the img so we can see what was  
        #left after it was applied 
        #frame = cv2.merge(mask)

    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= overlay)

    '''
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',overlay)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    cv2.destroyAllWindows()
    '''