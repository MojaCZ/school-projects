# -*- coding: cp1250 -*-
heslo = 'admin'
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
        password = raw_input('Zadejte heslo pro zapsání do datbáze: ')
        if password == heslo:
            name = raw_input('Zadejte jmeno uzivatele')
            if name:
                check = False
        else:
            if raw_input('Spatne heslo! Pro opakovani stisknete enter, pro konec napiste n') == 'n':
                print 'Konec snimani'
                break
    
            

    
             
        
                
