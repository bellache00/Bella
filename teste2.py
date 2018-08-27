import numpy as N
import serial as S
from cv2 import *
from modulo__main__ import * 




cap = VideoCapture(0)
while True:
    
    RET,leitura = cap.read()
    HSV = cvtColor(leitura, COLOR_BRG2HSV)
    resizeWindow('leitura', 600,600)
    
    intervalo_baixo = Intervalos().baixo_vermelho(0, 0, 0)
    intervalo_alto = Intervalos().alto_vermelho(0, 30, 60)
    
    mascara = inRange(HSV, intervalo_baixo, intervalo_alto)
    bitabit = bitwise_and(leitura, leitura, mask = mascara)
    
    
    #filtros
    kernel = N.ones((15, 15), N.uint64)
    gblur = GaussianBlur(mascara, (15, 15), 2)
    dilata = dilate(mascara, kernel, iterations = 1)
    medio =  medianBlur(dilata, 13)

    opening = morphologyEx(medio, MORPH_OPEN, kernel)
    closing = morphologyEx(medio, MORPH_CLOSE, kernel)

    cinza = cvtColor(bitabit, COLOR_BGR2GRAY)

    RET, limiar = threshold(cinza, 100, 255,
                           THRESH_BINARY_INV+THRESH_OTSU)
    _, contorno, hierarquia = findContours(grays,
                                              RETR_TREE,
                                              CHAIN_APPROX_TC89_L1)
    #Textos
    texto = list(Texto().texto())
    text = '300'
    #Textos
    
    putText(leitura, text, texto[1], int(texto[0]), 
                    int(texto[2]), texto[3],  int(texto[4]))

    imshow('imagem',leitura)
    #print(est)
    if waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
destroyAllWindows()

