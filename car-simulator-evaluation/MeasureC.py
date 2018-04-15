import math
import matplotlib.pyplot as plt

class Measurement:
    fileName = ""
    I = []
    time = []
    X = []
    Y = []
    speed = []
    steer = []
    throttle = []
    brake = []
    triggerCode = []

    # read file and fill arrays
    def __init__(self, fileName):
        self.fileName = fileName

        try:
            M = open(self.fileName, "r")
            text = M.read()
            text = text.split("\n")
            M.close
        except IOError:
            print ("Could not open file")
            quit()

        i = 0
        for line in text:
            if(line!=""):
                words = line.split(" ")
                if(float(words[8])>0.15):
                    self.I.append(i)
                    self.time.append(float(words[1])/1000)
                    self.X.append(float(words[2])/1000)
                    self.Y.append(float(words[4])/1000)
                    self.speed.append(float(words[8]))
                    self.steer.append(float(words[14]))
                    self.throttle.append(float(words[15]))
                    self.brake.append(float(words[16]))
                    self.triggerCode.append(int(words[36])*10)
                    i=i+1

    # print parameters
    def printPar(self):
        print ("fileName:       ", self.fileName)
        print ("I:              ", self.I[200:205])
        print ("time:           ", self.time[200:205])
        print ("X:              ", self.X[200:205])
        print ("Y:              ", self.Y[200:205])
        print ("speed:          ", self.speed[200:205])
        print ("steer:          ", self.steer[200:205])
        print ("throttle:       ", self.throttle[200:205])
        print ("brake:          ", self.brake[200:205])
        print ("triggerCode:    ", self.triggerCode[200:205])

    def retTime(self):
        return self.time

    def retPosition(self):
        return [self.X, self.Y]

    def retSpeed(self):
        return self.speed

    # return max speed and time of max speed as array [speed, time]
    def maxSpeed(self):
        MaxS = [0,0]
        for i in range(0, len(self.I)):
            if (self.speed[i] > MaxS[0]):
                MaxS[0] = self.speed[i]
                MaxS[1] = self.time[i]
        return MaxS

    # position of triggerCode points, return arrays of triggers [X, Y, I]
    def triggerArea(self):
        triggers = []
        isT = False
        for i in range (0, len(self.I)):
            if (self.triggerCode[i] != 0 | isT == False):
                T = []
                T.append(self.X[i])
                T.append(self.Y[i])
                T.append(self.I[i])
                triggers.append(T)
                isT = True
            elif (self.triggerCode[i] == 0):
                isT = False
        return triggers

    # brake and throttle in area of i trigger in time -10 +30 s
    # return array of arrays in format [time, brake, throttle]
    # return 0 if out of range
    def BrThArroundTrigger(self, k0):

        triggers = self.triggerArea()
        if (k0 > len(triggers)):
            return 0

        triggerArea = []    # will be returned
        n = triggers[k0][2]
        nM10 = n-10*125
        nP30 = n+30*125

        for i in range(nM10, nP30):
            triggerPoint = []
            triggerPoint.append(self.time[i])
            triggerPoint.append(self.brake[i])
            triggerPoint.append(self.throttle[i])
            triggerArea.append(triggerPoint)

        return triggerArea

    # average speed between first and the last trigger
    def averageBetweenTriggers(self):
        triggers = self.triggerArea()
        pathForAverage = 0
        # iterate from index of first trigger to index of last trigger every 10
        for i in range(triggers[0][2], triggers[len(triggers)-1][2]-10, 10):
            x = math.pow((self.X[i+10]-self.X[i]), 2)
            y = math.pow((self.Y[i+10]-self.Y[i]), 2)
            pathForAverage = pathForAverage + math.sqrt(x+y)

        timeForAverage = (self.time[triggers[2][len(triggers[2])-1]] - self.time[triggers[0][2]])/3600
        averageSpeed = pathForAverage/timeForAverage
        return [timeForAverage, averageSpeed]

    # plot speed and max speed
    def plotSpeed(self):
        maxSpeed = self.maxSpeed()
        plt.plot(self.time, self.speed, label="speed")
        plt.plot(maxSpeed[1], maxSpeed[0], marker="o", linestyle=" ", label="max speed")
        plt.legend()
        plt.xlabel("time [s]")
        plt.ylabel("speed [m/s]")
        plt.title("Speed and max speed")
        plt.show()

    # plot position and position of triggers
    def plotPosTriggers(self):
        triggers = self.triggerArea()
        triggers = self.tMatrix(triggers) # rows [trigger1] [trigger2] ... -> rows [X][Y][I] of triggers

        plt.plot(self.X, self.Y, label="position")
        plt.plot(triggers[0], triggers[1], marker="o", linestyle=" ", label="TriggerCode")
        plt.legend()
        plt.xlabel("x [km]")
        plt.ylabel("y [km]")
        plt.title("Position of TriggerCode")
        plt.show()

    # plot Brake and Throttle in area of triggers
    def plotBrThArroundTriggers(self, k0):
        TiBrTh = self.BrThArroundTrigger(k0)
        if(TiBrTh == 0):
            print("wrong trigger")
            return 0
        TiBrTh = self.tMatrix(TiBrTh)

        plt.plot(TiBrTh[0], TiBrTh[1], "r-", label="brake")
        plt.plot(TiBrTh[0], TiBrTh[2], "g-", label="throttle")
        plt.xlabel("time[s]")
        plt.ylabel("position")
        title = "Brake and Throttle in area of " + str(k0+1) + " trigger"
        plt.title(title)
        plt.legend()
        plt.show()

    # transport matrix
    def tMatrix(self, oldArray):
        newArray = []
        for i in range(0, len(oldArray[0])):
            newRow = []
            for j in range(0, len(oldArray)):
                newRow.append(oldArray[j][i])
            newArray.append(newRow)
        return newArray
