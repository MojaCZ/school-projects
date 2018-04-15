# -*- coding: cp1250 -*-
import numpy as np

heslo = '0'


#VYPOCET VZDALENOSTI
M_cm = [10,15,8,6,5,9,10,15]

#Luky:
#M_cm = [6.18911174785,12.2406876791,7.61031518625,8.84813753582,8.93982808023,8.25214899713,8.98567335244,6.32664756447]

#Kuba:
#M_cm = [5.94285714286,12.9828571429,7.77142857143,9.6,9.82857142857,8.36571428571,9.18857142857,5.48571428571]

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
    for j in range(1, len(M_cm)):
        procenta[i].append(float(M_cm[j-1]/float(databaze[i][j])*100))
        procentap[i].append(int(M_cm[j-1]/float(databaze[i][j])*100))
        rozdil[i].append(float(databaze[i][j])-float(M_cm[j-1]))
    print '%s %s' %(databaze[i][0], rozdil [i])
    
        
        
        

print '------------------------------------------------------' 
print 'Shody s uzivateli z databaze jsou: '

shoda = 1.0 #minimalni odchlka od databaze pro prirazeni identity
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
        password = ''
        while password != heslo:
            password = raw_input('Zadejte heslo pro zapsani do datbaze: ')
            if password == heslo:
                name = raw_input('Zadejte jmeno uzivatele')
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

print 'KONEC SNIMANI'
