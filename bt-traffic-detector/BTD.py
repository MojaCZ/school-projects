#!/usr/bin/env python3

# CALL WITH PYTHON3 !!!!
from sys import exit
import time
import subprocess
import sys
import os

sys.path.append('btdLibrary/')

import BTD_init
import BTD_Ubertooth


CWD, FILE_NAME_GROUP = "nil", "nil"
WAIT_TIME, NEW_FILE_INTERVAL, RPI, RPI_START_MEASURE, RPI_EXIT, RPI_READY, RPI_RUN, RPI_CATCHED = -1, -1, -1, -1, -1, -1, -1, -1

# initialization of program -> get variables from BTD.conf
initVars = BTD_init.init()

# from variables dictionary given by initialization constract variables
for var in initVars:
    exec("varT = type(" + var + ")")
    if type(initVars[var]) != varT:  # types in init doesn't mach with variables
        print("[err: BTD.py]: Heeeey don't even try mocking me, I can tell integer from string\nproblem is:\t", var, initVars[var])
        exit()
    try:
        exec(var + "=" + str(initVars[var]))
    except:
        exec(var + "=\"" + initVars[var] + "\"")

if RPI:
    import BTD_RPi
    RPI_O = BTD_RPi.RPi(RPI_START_MEASURE, RPI_EXIT, RPI_READY, RPI_RUN, RPI_CATCHED)
    print("RPI ON:")
    print("\tPower: ", RPI_O.Power(), "\tMeasure: ", RPI_O.Measure(), "\n\n")
    RPI_O.RPiReady()
    RPI_O.btdRunning(True)
    RPI_O.catched()
    time.sleep(1)

# if program is ended by user by KeyboardInterrupt
try:
    if RPI:
        RPI_O.btdRunning(False)
        RPI_O.catched()

    while True:
        if RPI and not RPI_O.Power:
            print("Program exited by user on switch state on GPIO\n\n")
            del RPi
            exit()

        if RPI and not RPI_O.Measure():
            continue

        if RPI:
            RPI_O.btdRunning(True)

        START_TIME = int(time.time())
        DETECTION = BTD_Ubertooth.Ubertooth(START_TIME, CWD, FILE_NAME_GROUP, WAIT_TIME)

        # create process
        process = subprocess.Popen(['ubertooth-rx', '-z'], stdout=subprocess.PIPE, bufsize=1)

        # loop detected devices
        for line in iter(process.stdout.readline, b''):

            if RPI and not RPI_O.Power():
                print("Program exited by user on switch state on GPIO")
                if RPI and RPI_O: del RPI_O
                process.stdout.close()
                exit()

            if RPI and not RPI_O.Measure():
                RPI_O.btdRunning(False)
                print("ending measurement on users command")
                break

            if (START_TIME + (NEW_FILE_INTERVAL * 60)) < int(time.time()):
                if RPI: RPI_O.btdRunning(False)
                print(START_TIME + (NEW_FILE_INTERVAL * 60), int(time.time()))
                print("ending measurement and starting new, interval expired\n\n")
                break

            written = DETECTION.getLine(line)
            if RPI and written:
                RPI_O.catched()

        # end process
        print("Ending Ubertooth process")
        process.stdout.close()
except KeyboardInterrupt:
    print("Program exited by user on event KeyboardInterrupt")
    if RPI and RPI_O: del RPI_O

# CLOSE PROCESS WITH
