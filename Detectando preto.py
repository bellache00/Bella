import cv2
import numpy as np



LimiarBinarizacao = 10

cap = cv2.VideoCapture(0)


while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#------------------------------------    
    #lower_red = np.array([0, 168, 120])
    #upper_red = np.array([180, 255, 255])
    lower_red = np.array([0, 0, 128])
    upper_red = np.array([180, 255, 255])
#-------------------------------------------
    #lower_2 = np.array([0, 148, 106])
    #upper_2 = np.array([180, 255, 255])
    lower_2 = np.array([0, 0, 70])
    upper_2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_2, upper_2)
    maskf = mask+mask2
#------------------------------------    
    kernel = np.ones((10, 10), np.uint8)
    
    dilation = cv2.dilate(maskf, kernel, iterations = 1)
    median =  cv2.medianBlur(maskf, 13)
    
    opening = cv2.morphologyEx(median, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(median, cv2.MORPH_CLOSE, kernel)
    
    res = cv2.bitwise_and(frame, frame, mask = median)
    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    FrameBinarizado = cv2.threshold(gray,LimiarBinarizacao,255,cv2.THRESH_BINARY)[1]
    FrameBinarizado = cv2.bitwise_not(FrameBinarizado)
    FrameBinarizado = cv2.dilate(FrameBinarizado, kernel, iterations = 1)

    __,contours, hierarchy = cv2.findContours(FrameBinarizado,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_TC89_L1)

    i = 0
    lista = []
    q = 0
    
    if contours:
        while i < len(contours[0]):
            if contours[0][i][0][1] == 479:
                lista.append(contours[0][i][0][0])
                q = 1
            i += 1

        if q == 1:
        
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
                    #ser.write('1'.encode())
                    
                
                #direita
            elif correcao >= 0:
                if int(max_p - min_p) > 250:
                    print("noventa graus _ e")


                else:
                    print("Esquerda")
                    #ser.write('0'.encode())
                    
                
                #esquerda
            else:
                print("Reto")
                #ser.write('2'.encode())
                
                #reto

    cv2.drawContours(frame, contours, -1, (0,255,0), 2)
    cv2.imshow('F.B.',FrameBinarizado)
    
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    cv2.imshow('resu',median)

    if cv2.waitKey(5) & 0xFF == ord('k'):
        break

cv2.destroyAllWindows()
cap.release()
