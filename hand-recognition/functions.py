import numpy as np
import cv2

#FUNKCE NA VYHLEDANI OBRYSU Z POLE ZADANEHO UZUVATELEM------------------------------------------
#X1 X2 jsou rozmery horizontalni
#Y1 Y2 jsou rozmery vertikalni
#im je obrazek na ktery hledani aplikuji
#color je barva ktera bude hranici
#shora - True pro hledani shora dolu, False pro hledani stranou
def Obrys (X1, X2, Y1, Y2, im, color, shora):
    if shora == False:
        X1, Y1 = Y1, X1
        X2, Y2 = Y2, X2
    #zjisteni smeru jakym hledam    
    if X1 > X2:
        smerx = -1
        X1 = X1-1
        X2 = X2+1
    else:
        smerx = 1
        X1 = X1+1
        X2 = X2-1
    if Y1 > Y2:
        smery = -1
        Y1 = Y1-1
        Y2 = Y2+1
    else:
        smery = 1
        Y1 = Y1+1
        Y2 = Y2-1
    #hlavni cyklus na prohledavani
    for j in range(X1,X2, smerx):
        ir = Y1
        for i in range(Y1,Y2, smery):
            if shora == True:
                if im[i,j] == color:
                    ir = i
            else:
                if im[j,i] == color:
                    ir = i
        #neberu v potaz kraje vyhledavaciho okenka            
        if Y1<Y2 and ir>Y1+2 and ir<Y2-2:
            if shora == True:
                im[ir,j] = 0
            else:
                im[j,ir] = 0
        if Y1>Y2 and ir>Y2+2 and ir<Y1-2:
            if shora == True:
                im[ir,j] = 0
            else:
                im[j,ir] = 0          
    return im

#FUNKCE NA ODDELENI RUKY OD ZBYTKU OBRAZKU
def Rozpoznej(X1,X2,Y1,Y2,img, hranice):
    for j in range(X1,X2):
        for i in range(Y1,Y2):
            if img[i,j] < hranice:
               img[i,j] = 200
            else:
               img[i,j] = 255
    return img

#FUNKCE PRO ZMENCENI DAT OBRYSU NA POTREBNA-----------------------------------------------------
#parametr je obrazek obrysu a vracim N matici 
def Obrys_vykresli (img):
    n = 0
    N = np.zeros(shape=(1,2))   #matice rozmeru 2 - i, j
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i,j] == 0:
                N = np.vstack([N, [i, j]])  #pridani prvku
                n = n+1
    N = N.astype(int)
    return N

