import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 168, 120])
    upper_red = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    kernel = np.ones((10, 10), np.uint8)
    dilation = cv2.dilate(res, kernel, iterations = 1)
    
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

    #smoothed = cv2.filter2D(dilation, -1, kernel)
    median =  cv2.medianBlur(dilation, 33)
    #blur =  cv2.GaussianBlur(dilation, (15,15), 0)
    #bilateral = cv2.bilateralFilter(dilation, 15, 75, 75)
    
    cv2.imshow('frame', frame)
    cv2.imshow('res', res)
    cv2.imshow('dilation', dilation)
    #cv2.imshow('mask', mask)
    #cv2.imshow('smoothed', smoothed)
    #cv2.imshow('blur', blur)
    cv2.imshow('median', median)
    #cv2.imshow('bilateral', bilateral)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
