# -*- coding: cp1250 -*-
import numpy as np
#VYPOCET VZDALENOSTI
M_cm = [8.94288714286, 14.982857142, 9.77142857143, 9.82857142857, 15.36571428571, 10.18857142857, 7.48571428571]


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
for i in range(0, len(databaze)):
    procenta.append([])
    rozdil.append([])
    for j in range(1, len(M_cm)):
        procenta[i].append(int(M_cm[j-1]/float(databaze[i][j])*100))
        rozdil[i].append(float(databaze[i][j])-int(M_cm[j-1]))
    
        
        
        

print '------------------------------------------------------' 
print 'Shody s uzivateli z databaze jsou: '

shoda = 3.5 #minimalni odchlka od databaze pro prirazeni identity
ID = 'Nikdo'
    
for i in range(0, len(databaze)):   #tisk procent shody s kazdym z databaze
    odchylka = []
    print databaze[i][0]
    odchylka = np.var(rozdil[i])    
    print ('Shoda jednotlivych bodu: %s Odchylka: %f ' % (procenta[i],odchylka))
    print ''
    
    if odchylka <= shoda:
        ID = databaze [i][0]    
       
    

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
    
#pridat co se stane po ulozeni nebo kdyz nechci uzivatele ulozit 

#print ('distance in px: %s', M_px)
#print ('distance in cm: %s', M_cm)

cv2.imshow('obrazek', frame)
cv2.imwrite('body.jpg', frame)

print 'KONEC SNIMANI'


cv2.waitKey()
cap.release()
