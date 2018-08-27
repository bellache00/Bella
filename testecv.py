import cv2


cap = cv2.VideoCapture(0)

_,frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.imshow('img', frame)
