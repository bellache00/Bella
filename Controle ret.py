import numpy as np
import cv2
import serial
 
ser = serial.Serial('COM8', 9600)


cap = cv2.VideoCapture(0)

while True:
    
    _, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lowerRed = np.array([175, 50, 100])
    upperRed = np.array([185, 300, 255])
    cv2.resizeWindow('frame', 600,600)

    #texto
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,100)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    #TEXTO

    
    mask = cv2.inRange(hsvImage, lowerRed, upperRed)
    result = cv2.bitwise_and(frame, frame, mask = mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((10, 10), np.uint8)
    dilation = cv2.dilate(gray, kernel, iterations = 5)

    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

    median =  cv2.medianBlur(dilation, 33)
    
    
    #parametros: imagem, valor do limiar, valor do pixel transformado, atribui o método de otsu
    _,gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    _, contours, hierarchy = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

      
    if contours:
        maxArea = cv2.contourArea(contours[0])
        contourId = 0
        i = 0
        for cnt in contours:
            if maxArea < cv2.contourArea(cnt):
                maxArea = cv2.contourArea(cnt)
                contourId = i
            i += 1
        cnt = contours[contourId]
        x,y,w,h = cv2.boundingRect(cnt)

        #diferença entre o ponto central do objeto e o referencial (em módulo [abs])
        text = str(int(abs(300 - (x+w/2))))
        #if(maxArea > 100.0):
            
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
        if x + w/2 < 250:
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

            #desenhar referencial
            cv2.line(frame, (250, 0), (250, 600), (255, 0, 0), 3)
            cv2.line(frame, (350, 0), (350, 600), (255, 0, 0), 3)
            cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (90,45,78), -1)
            cv2.line(frame, (300, 400), (int(x+w/2), 400), (255, 255, 0), 3)
            
            cv2.putText(frame, str(w), 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            ser.write('0'.encode())
            print(0)
        elif x + w/2 >= 350:
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

            #desenhar referencial
            cv2.line(frame, (250, 0), (250, 600), (255, 0, 0), 3)
            cv2.line(frame, (350, 0), (350, 600), (255, 0, 0), 3)

            #desenhar o centro do objeto 
            cv2.circle(frame, (int(x+w/2), int(y+h/2)), 5, (90,45,78), -1)

            #referencia para o controle P&D
            cv2.line(frame, (300, 400), (int(x+w/2), 400), (255, 255, 0), 3)

            #escrever distancia entre o referencial e o centro do objeto
            cv2.putText(frame, str(w), 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            ser.write('1'.encode())
            print(1)
        else:

            #desenhar referencial
            cv2.line(frame, (250, 0), (250, 600), (0, 255, 0), 3)
            cv2.line(frame, (350, 0), (350, 600), (0, 255, 0), 3)

            #escrever distancia entre o referencial e o centro do objeto
            cv2.putText(frame, str(w), 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            #ser.write('2'.encode())
    
    cv2.imshow('frame', frame)
    cv2.imshow('result', result)
    #cv2.imshow('dilation', dilation)
    cv2.imshow('median', median)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
