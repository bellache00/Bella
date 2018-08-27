import numpy as np
import cv2
import serial

 
ser = serial.Serial('COM8', 9600)


cap = cv2.VideoCapture(0)

while (True):
    
    _, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lowerRed = np.array([0, 0, 0])
    upperRed = np.array([30, 35, 45])
    cv2.resizeWindow('frame', 600,600)

    #texto
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,100)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    #TEXTO

    #texto2
    font2                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText2 = (10,100)
    fontScale2              = 1
    fontColor2              = (255,255,255)
    lineType2               = 2
    #TEXTO

    
    mask = cv2.inRange(hsvImage, lowerRed, upperRed)
    result = cv2.bitwise_and(frame, frame, mask = mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((15, 15), np.uint64)

    #cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
    
    #cotoro = cv2.GaussianBlur(mask, (15, 15), 2)

    cotoro = cv2.dilate(mask, kernel, iterations = 1)

    median =  cv2.medianBlur(cotoro, 13)
    
    opening = cv2.morphologyEx(cotoro, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(cotoro, cv2.MORPH_CLOSE, kernel)

    #gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
     
    #parametros: imagem, valor do limiar, valor do pixel transformado, atribui o método de otsu
    _,gray = cv2.threshold(median, 100, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    _, contours, hierarchy = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

    i = 0
    lista = []
    q = 0
    
    if contours:
        while i < len(contours[0]):
            if contours[0][i][0][1] == 300:
                lista.append(contours[0][i][0][0])
                q = 1
            i += 1

        if q == 1:

            cv2.line(frame, (0, 300), (639, 300), (255, 0, 0), 3)
            max_p = max(lista)
            min_p = min(lista)
            
            centro = 320

            centro_o = (max_p + min_p)/2

            correcao = centro - centro_o

            if correcao < 0:
                if int(max_p - min_p) > 250:
                   print("noventa graus _ d")

                else:
                    print("Direita")
                    ser.write('1'.encode())
                    
                
                #direita
            elif correcao >= 0:
                if int(max_p - min_p) > 250:
                    print("noventa graus _ e")


                else:
                    print("Esquerda")
                    ser.write('0'.encode())
                    
                
                #esquerda
            '''else:
                print("Reto")
                ser.write('2'.encode())
                
                #reto'''
                
                
    cv2.imshow('frame', frame)
    #cv2.imshow('gradient', gradient)
    #cv2.imshow('result', result)
    #cv2.imshow('dilation', dilation)
    cv2.imshow('median', median)
    #cv2.imshow('mask', mask)
    #cv2.imshow('cotoro', cotoro)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
