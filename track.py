import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h1,s1,v1 = 100,100,100
h2,s2,v2 = 100,100,100

# Creating track bar
cv2.createTrackbar('h1', 'result',0,180,nothing)
cv2.createTrackbar('s1', 'result',0,255,nothing)
cv2.createTrackbar('v1', 'result',0,255,nothing)
cv2.createTrackbar('h2', 'result',0,180,nothing)
cv2.createTrackbar('s2', 'result',0,255,nothing)
cv2.createTrackbar('v2', 'result',0,255,nothing)

while(1):

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h1 = cv2.getTrackbarPos('hl','result')
    s1 = cv2.getTrackbarPos('sl','result')
    v1 = cv2.getTrackbarPos('vl','result')
    h2 = cv2.getTrackbarPos('hu','result')
    s2= cv2.getTrackbarPos('su','result')
    v2 = cv2.getTrackbarPos('vu','result')

    # Normal masking algorithm
    lower_blue = np.array([h1,s1,v1])
    upper_blue = np.array([h2,s2,v2])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)
    

    result = cv2.bitwise_and(frame,frame,mask = mask)

    cv2.imshow('result',result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()
