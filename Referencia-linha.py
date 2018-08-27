import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([8, 130, 0])
    upper_red = np.array([23, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    
    cv2.resizeWindow('frame', 600,600)
    
    cv2.line(frame, (250, 0), (250, 600), (255, 0, 0), 3)
    cv2.line(frame, (350, 0), (350, 600), (255, 0, 0), 3)
    
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
        
    if cv2.waitKey(5) & 0xFF == ord('k'):
        break

cv2.destroyAllWindows()
cap.release()
