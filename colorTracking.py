import cv2
import numpy as np


def trackGreenTarget(debug=False):
    cap = cv2.VideoCapture(0)
    #print cap.isOpened()
    if not cap.isOpened():
        print "Error Establishing Video Feed!"
        return

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
    	cv2.circle(overlay, (int(x), int(y)), 2, (255, 255, 255), 20)
        if debug==False:
            return (int(x),int(y))
        else:
            print x,y
    if debug==True:
        return (frame,mask,overlay)
            

        #frame = cv2.add(frame, overlay)
        #add the thresholded image back to the img so we can see what was  
        #left after it was applied 
        #frame = cv2.merge(mask)

    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= overlay)

def debug():
    cap = cv2.VideoCapture(-1)
    print cap.get(3)
    print cap.get(4)
    #print cap.isOpened()
    if not cap.isOpened():
        print "Error Establishing Video Feed!"
        return
    while(1):
       

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
            cv2.circle(overlay, (int(x), int(y)), 2, (255, 255, 255), 20)
            print x,y
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res',overlay)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destoyAllWindows()
    
#trackGreenTarget(True)

if __name__ == '__main__':
    debug()
