import cv2
import numpy as np
import copy
import math
import time
from functions import *

heslo = '0'

# KONFIGURACE OBLASTI PRO VYHLEDAVANI
hranice = 220    #pro nastaveni hranice svetelnosti ruky [sirka od do, vyska od do] [0,0] je vlevo nahore
A = [[50,170,300,450],
      [190,300,300,420],
      [150,270,60,210],
      [250,320,180,300],
      [250,350,10,200],
      [320,400,180,300],
      [350,470,10,200],
      [400,455,180,325],
      [450,570,100,250]]

print 'pro zaznamenani videa stitskni \'y\' pro ukonceni \'e\''
cap = cv2.VideoCapture(2)   #video capture source camera
obrys = cv2.imread('obrys_velky.jpg', cv2.IMREAD_GRAYSCALE)
N = Obrys_vykresli(obrys)

#SMYCKA VIDEA A SNIMANI FOTKY
chyba = 0
while True:
    ret,frame = cap.read()      #return a single frame in variable frame
    
    if cv2.waitKey(1) & 0xFF == ord('y'):   #save in pressing 'y'
        cv2.destroyAllWindows()
        break
    
    if cv2.waitKey(1) & 0xFF == ord('e'):   #end in pressing 'e'
        print '[INFO]: THE END'
        cv2.destroyAllWindows()
        exit()
        break
        

    if frame is not None:   #podminka pokud neni zapnuta kamera
        chyba = 0
        for m in range(1, N.shape[0]):
            frame[N[m][0],N[m][1]] = 0
        
        for i in range (0, frame.shape[0], 100):  #vykresleni kruhu po 100px
            for j in range (0, frame.shape[1], 100):
                cv2.circle(frame,(j, i),3,(125,0,100),-1)

        for i in range (0, frame.shape[0]):
            frame[i, frame.shape[1]-20] = 255,0,0           

        for i in range (0, len(A)): #vykresleni oblasti zajmu (obdelnik a text)
            if i % 2 == 0:
                cv2.rectangle(frame, (A[i][0], A[i][2]), (A[i][1], A[i][3]),(0,255,0),1)
            else:
                cv2.rectangle(frame, (A[i][0], A[i][2]), (A[i][1], A[i][3]),(0,0,255),1)
                
            cv2.putText(frame,('A'+`i+1`),(A[i][0],A[i][2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))
        

        cv2.imshow('video', frame)
    #pokud neni zapnuta kamera a snimky se nenacitaji, tak ukoncim program... a VYPNU VSECHNY OTEVRENE OBRAZKY!! a kdyz nefunguje ani pak vytahnout a zase zasunout kameru a znova spustit    
    if frame is None:
        if chyba > 5:
            print '[INFO]: camera is not set!!!'
            exit()
        chyba = chyba+1
        print '[INFO]: chyba kamery: ', chyba

gray = copy.deepcopy(frame)
gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

#NACTENI SCALE Z CAR VZDALENYCH 20CM VPRAVO NA PAPIRE
j = gray.shape[1]-20
for i in range(int(gray.shape[0]/float(2)), gray.shape[0], 1):
    if gray[i,j] < 40:
        S1 = i-gray.shape[0]/float(2)
        break
for i in range(gray.shape[0]/2, 0, -1):
    if gray[i,j] < 40:
        S2 = gray.shape[0]/float(2) - i
        break

S_px = S1+S2    #pixelu zmereno obrazkem 
S_cm = 16       #vim cm zmerene na papire             #M_cm = M_px/S_px * S_cm
    

#odstraneni kruhu
r = 150
S = [int(gray.shape[0]/float(2))+50, int(gray.shape[1]/float(2)+50)]
for i in range(0,gray.shape[0]):
    for j in range(0, gray.shape[1]):
        l = math.sqrt((S[0]-i)**2 + (S[1]-j)**2)
        if l<r and gray[i,j] < 180:
            gray[i,j] = 0
        elif l<r:
            gray[i,j] = 255

r = 70
S = [gray.shape[0]-110, 250]
for i in range(0,gray.shape[0]):
    for j in range(0, gray.shape[1]):
        l = math.sqrt((S[0]-i)**2 + (S[1]-j)**2)
        if l<r and gray[i,j] < 180:
            gray[i,j] = 0
        elif l<r:
            gray[i,j] = 255

#odstraneni ruky
for i in range(0,gray.shape[0]):
    for j in range(0, gray.shape[1]):
        if gray[i,j] < 70:
            gray[i,j] = 0
        else:
            gray[i,j] = 255

#cv2.imshow('1', gray)

#ODDELENI RUKY OD HRANICE
gray = Rozpoznej(0,gray.shape[1],0,gray.shape[0],gray,hranice)

#OZNACENI HRAN
for i in range(1, len(A)):
    gray = Obrys(A[i][0],A[i][1],A[i][2],A[i][3], gray, 255, True)
gray = Obrys(A[0][0],A[0][1],A[0][2],A[0][3], gray, 255, False)

#cv2.imshow('2', gray)

#NALEZENI MAXIM
points = np.zeros(shape=(len(A), 2))
points = points.astype(int)
                                #potom prohodit všechny matice (takhle to funguje ale nelibi se mi to)
for m in range(1,len(A),2):     #maxima pro spodni casti mezi prsty
    I = 0
    J = 0
    for j in range(A[m][0],A[m][1]):
        for i in range(A[m][2],A[m][3]):
            if gray[i,j] == 0 and i>I:
                I = i
                J = j
    points[m] = [I, J]
                
for m in range(2,len(A),2):     #maxima pro vrsky prstu
    I = A[m][3]
    J = 0
    for j in range(A[m][0],A[m][1]):
        for i in range(A[m][2],A[m][3]):
            if gray[i,j] == 0 and i<I:
                I = i
                J = j
    points[m] = [I, J]

I = 0
J = A[0][1]
for i in range(A[0][2],A[0][3]):    #maximum pro palec
    for j in range(A[0][0],A[0][1]):
        if gray[i,j] == 0 and j<J:
            I = i
            J = j
points[0] = [I, J]

#VYKRESLENI VYSLEDKU
for m in range(0,len(points)):  #vykresleni a popis bodu
    cv2.circle(frame,(points[m][1], points[m][0]),5,(255,0,0),-1)
    cv2.putText(frame,('P'+`m`),(points[m][1]-10, points[m][0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))

for m in range(0,len(points)-1):    #vykresleni a popis spojnic
    cv2.line(frame,(points[m][1], points[m][0]),(points[m+1][1], points[m+1][0]),(0,0,255),1)
    cv2.putText(frame,('L'+`m`),(min(points[m][1],points[m+1][1]) + abs(points[m][1]-points[m+1][1])/2, min(points[m][0],points[m+1][0]) + abs(points[m][0]-points[m+1][0])/2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))

#cv2.imshow('3', frame)
cap.release()

#VYPOCET VZDALENOSTI
M_px = []
M_cm = []
for m in range(0,len(points)-1):
    M_px.append( math.sqrt((points[m][0]-points[m+1][0])**2+(points[m][1]-points[m+1][1])**2) )
    M_px[m] = round(M_px[m])
    M_cm.append( S_cm/float(S_px) * M_px[m] )

#DATABÁZE NACTENI
file = open('databaze.txt', 'r')
databaze = file.readlines()
for i in range(0,len(databaze)):
    databaze[i] = databaze[i].strip()
    databaze[i] = databaze[i].split(';')
file.close()

#OVERENI RUKY
procenta = []
rozdil = []
procentap = []
for i in range(0, len(databaze)):
    procenta.append([])
    procentap.append([])
    rozdil.append([])
    for j in range(2, len(M_cm)):
        procenta[i].append(float(M_cm[j-1]/float(databaze[i][j])*100))
        procentap[i].append(int(M_cm[j-1]/float(databaze[i][j])*100))
        rozdil[i].append(float(databaze[i][j])-float(M_cm[j-1]))
    #print '%s %s' %(databaze[i][0], rozdil [i])
    
        
        
        

print '------------------------------------------------------' 
print 'Shody s uzivateli z databaze jsou: '

shoda = 0.05 #minimalni odchlka od databaze pro prirazeni identity
ID = 'Nikdo'


for i in range(0, len(databaze)):   #tisk procent shody s kazdym z databaze
    odchylka = []
    print databaze[i][0]
    odchylka = np.var(rozdil[i])    
    print ('Shoda jednotlivych bodu: %s Odchylka: %f ' % (procentap[i],odchylka))
    print ''
    
    if odchylka <= shoda:
        ID = databaze [i][0]
        shoda = odchylka
       
    

print '------------------------------------------------------'

print 'Identifikovan: ', ID

if ID == 'Nikdo':


    #chci zapsat uzivatele?
    check = True
    while check:
        CH = raw_input('Chcete zadat noveho uzivatele? Y/N')
        if (CH=='Y' or CH=='N' or CH=='y' or CH =='n'):
            check = False
        
    #zadej jmeno uzivatele
    if CH == 'Y' or CH == 'y':
        check = True
        password = 0
        while password != heslo:
            password = raw_input('Zadejte heslo pro zapsani do datbaze: ')
            if password == heslo:
                name = raw_input('Zadejte jmeno uzivatele')
                if name:
                    check = False
            else:
                if raw_input('Spatne heslo! Pro opakovani stisknete enter, pro konec napiste n') == 'n':
                    print 'Konec snimani'
                    exit()
            
        #ZAPIS DO DATABAZE       
        file = open('databaze.txt', 'a')
        file.write('\n%s;'%name)
        for i in range(0, len(M_cm)):
            file.write('%s;'%M_cm[i])
            if i == len(M_cm):
                file.write(M_cm[i])
        file.close()
        print 'Uzivatel pridan'
    


#print ('distance in px: %s', M_px)
print ('distance in cm: ', M_cm)


#cv2.imwrite('body.jpg', frame)
cv2.imshow('obrazek', frame)


cv2.waitKey()
cap.release()

check = True
while check:
    CH = raw_input('Chcete opakovat identifikaci? Y/N')
    if (CH=='Y' or CH=='N' or CH=='y' or CH =='n'):
        check = False

    if CH == 'Y' or CH == 'y':
        print '---------------------------------------------------------------------'
        print '---------------------------------------------------------------------'
        execfile('ruka_video.py')
    else:
        print 'KONEC SNIMANI'
        

    
