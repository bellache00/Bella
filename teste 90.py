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

    cotoro = cv2.dilate(mask, kernel, iterations = 5)

    median =  cv2.medianBlur(cotoro, 13)
    
    opening = cv2.morphologyEx(cotoro, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(cotoro, cv2.MORPH_CLOSE, kernel)

    #gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
     
    #parametros: imagem, valor do limiar, valor do pixel transformado, atribui o método de otsu
    _,gray = cv2.threshold(median, 100, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    _, contours, hierarchy = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

    i = 0
    lista_h = []
    lista_v1 = []
    lista_v2 = []
    lista_h2 = []
    
    if contours:

        qtd = len(contours[0])

        while i < qtd:
            if contours[0][i][0][1] == 479:
                lista_h.append(contours[0][i][0][0])

            if contours[0][i][0][1] == 0:
                lista_h2.append(contours[0][i][0][0])

            valor_x = int(contours[0][i][0][0])
            valor_y = int(contours[0][i][0][1])
            
            if valor_x < 80 and (valor_y >= 50 and valor_y <= 200):
                lista_v1.append(contours[0][i][0][1])

            if valor_x >= 620 and (valor_y >= 50 and valor_y <= 200):
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

            q = 0
            a = 0
            
            if len(lista_v2) != 0:
                max_v2 = max(lista_v2)
                min_v2 = min(lista_v2)
                tamanho_v2 = max_v2 - min_v2

                q = 1

            if len(lista_v1) != 0:
                max_v1 = max(lista_v1)
                min_v1 = min(lista_v1)
                tamanho_v1 = max_v1 - min_v1

                a = 1

            if (q == 1 or a == 1) and len(lista_h2) != 0:
                lowerRed = np.array([30, 100, 100])
                upperRed = np.array([80, 255, 255])
                mask2 = cv2.inRange(hsvImage, lowerRed, upperRed)

                _, contours, hierarchy = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
                
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
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

                    if x + w/2 > 320:
                        print("Noventa graus a direita")
                    elif x + w/2 < 320:
                        print("Noventa graus a esquerda")

                else:
                
                    if q == 0 and a == 1:
                        print("Noventa Graus a esquerda_1")

                    elif q == 1 and a == 0:
                        print("Noventa Graus a direita_1")

                    elif q == 0 and a == 0:

                        if correcao_h < -30:
                            print("Direita")

                        if correcao_h > 30:
                            print("esquerda")

                        else:
                            print("Reto")

                    else:
                        print("cruzamento")
                        
                 
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
