import numpy as np
import cv2
import copy
import workingPort

#originally 20
SENSITIVITY = 30
#originally 10
BLUR_SIZE = 20

def searchForMotion(thresholdImg, cameraFeed):
    detected = False
    xpos=0
    ypos =0
    #Edit - pointless copy
    temp = copy.deepcopy(thresholdImg)
    
    _, contours0, hierarchy = cv2.findContours( temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]
    #print contours
    if (len(contours0)>0):
        detected = True
    else:
        detected = False
    
    if detected:
        largestContour = contours0.pop()
        roiContour = []
        #print "largest",largestContour
        (x, y, w, h) = cv2.boundingRect(largestContour)
        xpos = x + w/2
        ypos = y + h/2
        
        target = (xpos, ypos)
        cv2.circle(cameraFeed,(xpos, ypos),20,(0,255,0), 2)
        return (xpos,ypos)

def main():
    detected = False
    debug = False

    camera = cv2.VideoCapture(0)
    print camera.isOpened()
    # if not camera.isOpened():
    #     print "Error Establishing Video Feed!"
    #     return -1
        
    while(True):
        (acquiered,frame1) = camera.read()
        
        grayImg1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        (_,frame2) = camera.read()
        grayImg2 = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        differenceImg = cv2.absdiff(grayImg1,grayImg2)
        (_ , thresholdImg) = cv2.threshold(differenceImg,  SENSITIVITY, 255, cv2.THRESH_BINARY)
        if debug:
            cv2.imshow("difference",differenceImg)
            cv2.imshow("threshold",thresholdImg)
        else:
            cv2.destroyWindow("difference")
            cv2.destroyWindow("threshold")
        thresholdImg = cv2.blur(thresholdImg, (BLUR_SIZE,BLUR_SIZE))
        (_,thresholdImg) = cv2.threshold(thresholdImg,  SENSITIVITY, 255, cv2.THRESH_BINARY)
        if debug:
            cv2.imshow("final",thresholdImg)
        else:
            cv2.destroyWindow("final")
        (xTarget, yTarget) = searchForMotion(thresholdImg,frame1)
        manipulator = SSC32()
        cv2.imshow("frame1", frame1)
        keyPress = cv2.waitKey(10)
        if keyPress==27:
            break
        elif keyPress == 100:
            debug = debug ^ True
    
    camera.release()

main()
        
                