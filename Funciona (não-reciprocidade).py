import numpy as np
import cv2
#import serial
import time
 
#ser = serial.Serial('COM10', 9600)

cap = cv2.VideoCapture(0)

while (True):
    
    _, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lowerRed = np.array([0, 0, 0])
    upperRed = np.array([180, 255, 78])
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
    #result = cv2.bitwise_and(frame, frame, mask = mask)

    #gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((15, 15), np.uint64)

    #cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
    
    #cotoro = cv2.GaussianBlur(mask, (15, 15), 2)

    cotoro = cv2.dilate(mask, kernel, iterations = 4)

    median =  cv2.medianBlur(cotoro, 13)
    
    #opening = cv2.morphologyEx(cotoro, cv2.MORPH_OPEN, kernel)
    #closing = cv2.morphologyEx(cotoro, cv2.MORPH_CLOSE, kernel)

    #gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
     
    #parametros: imagem, valor do limiar, valor do pixel transformado, atribui o método de otsu
    _,gray = cv2.threshold(median, 100, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    result = cv2.bitwise_not(frame, frame, mask = gray)
    cinza = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

    i = 0
    lista_h = []
    lista_v1 = []
    lista_v2 = []

    
    if contours:

        qtd = len(contours[0])

        while i < qtd:
            if contours[0][i][0][1] > 200 and contours[0][i][0][1] < 210:
                lista_h.append(contours[0][i][0][0])

            valor_x = int(contours[0][i][0][0])
            
            if valor_x < 80:
                lista_v1.append(contours[0][i][0][1])

            if valor_x == 639:
                lista_v2.append(contours[0][i][0][1])
                
            i += 1
            
        if len(lista_h) != 0:

            max_h = max(lista_h)
            min_h = min(lista_h)

            centro = 320

            centro_o = (max_h + min_h  )/2

            correcao_h = centro - centro_o

            cv2.line(frame, (290, 0), (290, 479), (255, 0, 0), 3)
            cv2.line(frame, (350, 0), (350, 479), (255, 0, 0), 3)

            cv2.line(frame, (320, 400), (int(centro_o), 400), (0, 0, 255), 3)

            if correcao_h < -30:

                if len(lista_v2) != 0:
                    max_v2 = max(lista_v2)
                    min_v2 = min(lista_v2)
                    tamanho_v2 = max_v2 - min_v2

                    print(max_v2)
                    print(min_v2)

                    if tamanho_v2 > 40:
                       print("noventa graus _ d")

                else:
                    print("Direita")
                    #ser.write('1'.encode())
                    #time.sleep(0.2)
                
                #direita
            elif correcao_h >= 30:
                if len(lista_v1) != 0:
                    max_v1 = max(lista_v1)
                    min_v1 = min(lista_v1)
                    tamanho_v1 = max_v1 - min_v1

                    if tamanho_v1 > 40:
                        print("noventa graus _ e")
                    
                else:
                    print("Esquerda")
                    #ser.write('0'.encode())
                    #time.sleep(0.2)
                
                #esquerda
            else:
               print("Reto")
               #ser.write('2'.encode())
                
                #reto
                
                
    cv2.imshow('frame', frame)
    #cv2.imshow('gradient', gradient)
    #cv2.imshow('result', result)
    #cv2.imshow('dilation', dilation)
    cv2.imshow('median', result)
    #cv2.imshow('mask', mask)
    #cv2.imshow('cotoro', cotoro)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
