#!/usr/bin/env python3

import sys
import time
from sys import exit

sys.path.append('btdLibrary/')
import BTD_Process

def main():

    if len(sys.argv) <= 1:
        print("[ERROR]: some flag is needed\n")
        printHelp()
        exit()

    # available flags
    KNOWN_FLAGS = ["-h","-p", "-co", "-ci", "-o"]
    FIRST_FLAG = ""
    SECOND_FLAG = ""

    # current argument position (1-second position ...), 0-first is function name, I'll scip this one
    ARG_POS = 1

    # FIRST FLAG ARGUMENT --------------------------------------------
    # read second argument
    FLAG = sys.argv[ARG_POS]
    ARG_POS = ARG_POS + 1

    # check if argument starts with -
    if FLAG[0] is not "-":
        print("invalid flag format, missing \"-\": ", flag)
        exit()

    # check if flag is known
    knownFlag = False
    for F in KNOWN_FLAGS:
        if F == FLAG:
            knownFlag = True
            break
    if not knownFlag:
        print("unknown flag: ", flag, "\nuse -h for help")
        printHelp()
        exit()

    if FLAG == "-h":
        printHelp()
    else:
        FIRST_FLAG = FLAG

    # SECOND FLAG ARGUMENT --------------------------------------------
    FLAG = sys.argv[ARG_POS]
    if FLAG[0] == "-" and isINT(FLAG[1:]):
        if int(FLAG[1:]) <= 0:
            print("second argument MUST be positive integer")
            exit()
        SECOND_FLAG = int(FLAG[1:])
        ARG_POS = ARG_POS + 1

    # NOW FILES
    for arg in sys.argv[ARG_POS:]:

        if not arg.endswith(".txt") and not checkBtdFile(arg): continue
        if not checkBtdFile(arg): continue

        D = BTD_Process.dataProcess(arg)

        if FIRST_FLAG == "-p":
            print(arg, "\n",D.retFileInfo())
            D.printDevices()
            print("\n")

        if FIRST_FLAG == "-co":
            D.printMatrix(D.countOccurancy())
            print()

        if FIRST_FLAG == "-ci":
            if SECOND_FLAG == "":
                print("Interval not given (second flag)")
            D.printMatrix(D.countIntervals(SECOND_FLAG))
            print()

        if FIRST_FLAG == "-o":
            D.printMatrix(D.order())

def isINT(s):
    try:
        int(s)
        return True
    except:
        return False

# give filename with suffix .txt, check if first line is "start time: [" and endswith "]"
def checkBtdFile(fileName):
    with open(fileName, 'r') as f:
        for line in f:
            if line.startswith("start time: [") and line.endswith("]\n"):
                return True
            return False
    return False

def printHelp():
    print("This is Program for processing measurement, was developed for bluetooth detector data processing\n\n")
    print("dataProcess [option] [file ...]\n")
    print("options:")
    print("\t-p\t: for printing all measured data from given files")
    print("\t-h\t: print this message and exit")
    print("\t-co\t: count intervals")
    print("\t-ci\t: count occurancy")
    print("\t-o\t: order")
    exit()

if __name__ == "__main__":
    main()
