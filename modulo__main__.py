from cv2 import *
import numpy as N

if __name__ == '__main__':
    pass

class Intervalos:

    def __init__(self):
        pass
    
    def baixo_vermelho(self, x = 0, y = 0, z = 0):
        inter_bax = N.array([x, y, z])
        return inter_bax
    
    def alto_vermelho(self, x = 0, y = 25, z = 30):
        inter_alt = N.array([x, y, z])
        return inter_alt
        
        
    def preto(self, inter_bax, inter_alt):
        pass

class Funcionalidades:

    def __init__(self):
        pass

    def formato(sel, leitura, x, y):
        resizeWindow("{}".format(leitura), x, y)

class Texto:

    def __init__(self):
        pass

    def texto(self, fonte = str(FONT_HERSHEY_SIMPLEX),
              posi_esquerda = (10,100),
              escala = str(1),
              cor = (255,255,255),
              tipo_linha = str(2)):
        
        return(fonte, posi_esquerda, escala, cor, tipo_linha)
    
        

    
        












        
    
    
    
    
    
