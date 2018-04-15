# list of variables which should be in BTD.conf file
initVarList =  [["CWD", False],
["FILE_NAME_GROUP", False],
["WAIT_TIME", False],
["NEW_FILE_INTERVAL", False],
["RPI", False],
["RPI_START_MEASURE", False],
["RPI_EXIT", False],
["RPI_READY", False],
["RPI_RUN", False],
["RPI_CATCHED", False]]

# check if name of variable is in initVarList, if is return 1 and change value to True (variable was chacked)
def checkOccurence(varName):
    for var in initVarList:
        if var[0] == varName:
            var[1] = True
            return 1
    return 0

# check if values in given list are not same
def multipleValue(List):
    for i in range(0, len(List)):
        for j in range(i+1, len(List)):
            if List[i] == List[j]:
                return True
    return False

# I don't want any blank strings or negative variables
def validateVars(initVars):
    allowedGPIO = [7, 11, 12, 13, 15, 16, 18, 22]
    for var in initVars:

        # check if value is negative int or empty string
        if isinstance(initVars[var], int) and initVars[var] < 0: # is int and negative
            print("[err: BTD_functions.py]: What? What is that weird thing before integer? what are you trying to feed me up with?\nProblem is:\t", var, initVars[var])
            exit()
        elif initVars[var]=="":
            print("[err: BTD_functions.py]: Heeeey there, give mi something to eat, I don't want just blank string\nProblem is:\t", var, initVars[var])
            exit()

        # if given number of GPIO port is allowed
        if var.startswith("RPI_"):
            if initVars[var] not in allowedGPIO:
                print("[err: BTD_functions.py]: No that way, you will burn Raspberry\nProblem is:\t", var, initVars[var])
                exit()

    # if some of RPI_ values is equal to other RPI_ value
    RPI_Values = [initVars["RPI_START_MEASURE"], initVars["RPI_EXIT"], initVars["RPI_READY"], initVars["RPI_RUN"], initVars["RPI_CATCHED"]]
    if multipleValue(RPI_Values):
        print("[err: BTD_functions.py]: Hi, We've got a problem here, You can't have two RPi GPIO ports equal values\nProblem is:\t", List[i], " = ", List[j])
        exit()

    return 1

def init():
    initVars = {}
    try:
        with open("BTD.conf", 'r') as f:
            for l in f:
                l = l.strip()
                # if line isn't blanc and if is not comment line
                if l != "" and l[0]!='#':
                    # split on name and value
                    var = l.split("=")

                    # strip white spaces
                    for i in range(0, len(var)):
                        var[i] = var[i].strip()
                        if(len(var[i].split())>1):
                            print("[err: BTD_functions.py]: There is an issue with reading BTD.conf file, in one lines are too much argumets for example (RPI = 1 5)\nThe part I don't like is:\t", var[i])
                            exit()

                    # check if variable is in initVarList
                    if not checkOccurence(var[0]):
                        print("[err: BTD_functions.py]: ouch, there seems to be a new variable I don't know, hmmm I don't like it at all:\n\t", var)
                        exit()


                    # everything ok, add to dictionary of vars
                    try:
                        initVars.update({var[0]:int(var[1])})
                    except:
                        initVars.update({var[0]:var[1]})

        # if some variable is missing in BTD.init
        for var in initVarList:
            if not var[1]:
                print("[err: BTD_functions.py]: OH NO, I'm missing", var[0], " variable, I loved this one most of all")
                exit()
        validateVars(initVars)
        return(initVars)

    except IOError:
        print("[err: BTD_functions.py]: Sorry, there is no BTD.conf file so I can configure myself")
        return 0
    return 0
