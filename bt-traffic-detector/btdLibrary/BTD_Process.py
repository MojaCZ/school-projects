import sys
import time
from sys import exit

class dataProcess:
    fileInfo = ""
    devicesList = []

    def __init__(self, fileName):
        devices = []
        with open(fileName, 'r') as f:
            for l in f:
                self.fileInfo = l.strip()
                break
            for line in f:
                catch = line.split(' ')
                LAP = catch[0].strip()
                time = catch[1].strip()
                time = time.split(':')
                time = int(time[0])*3600+int(time[1])*60+int(time[2])
                NEW = [LAP, time]
                devices.append(NEW)
        self.devicesList = devices

    def formatTime(self, T):
        h = str(int((T/3600)%24))
        m = str(int((T/60)%60))
        if int((T)%60) > 0:
            s = str(int((T)%60))
        else:
            s = "00"
        sT = h + ":" + m + ":" + s
        return sT

    def retFileInfo(self):
        return self.fileInfo

    # Print lines containing BT address from file
    def printDevices(self):
        for device in self.devicesList:
            print(device[0], device[1])
            # print(device[0], self.formatTime(device[1]))----------------------------------------------------------------------! ! ! ! ! ! !

    # countOccurancy will count occurancy of records (lines) by given index column
    # it will return list of record with counted occurancy
    def countOccurancy(self, index=0):
        if index >= len(self.devicesList[0]) or index < 0:
            return 0

        count = []
        SUM = int

        for i in range(0, len(self.devicesList)):
            isIN = False
            for el in count:
                if self.devicesList[i][index] == el[index]:
                    isIN = True
                    el[len(el)-1] = el[len(el)-1]+1
                    break
            if isIN == False:
                new = [self.devicesList[i][index], 1]
                count.append(new)
        return count

    # countIntervals is function, which loops over list of records (one in line),
    # records MUST be sorted by time column
    # take given time (column with given index)
    # don't loop through intervals and try every, count how many must skip to fund suitable for another record
    # it will include blank intervals as well, if you don't want include it, in code uncomment > 1 and comment > 2
    def countIntervals(self, interval, index=1):
        if index >= len(self.devicesList[0]) or index < 0:
            return 0

        start = 0   # start of interval
        end = start + interval  # end of interval
        occurancy = []  # list of intervals wit count of devices occurancy [start end count]
        count = 0

        # for every device
        for el in self.devicesList:
            jump = int((int(el[index])-start)/interval) #give integer of how many intervals the number jump cross

            # in case one device skip multiple intervals range through blank intervals
            for i in range(0,jump):
                newInterval = [self.formatTime(start), self.formatTime(end), count]
                # if count < 1:                       # > 1
                #     occurancy.append(newInterval)   # > 1
                occurancy.append(newInterval)   # >2
                start = end
                end = start + interval
                count = 0
            count = count + 1   # add one to next interval (counted interval of device)

        # when last element, add last interval as well
        newInterval = [self.formatTime(start), self.formatTime(end), count]
        occurancy.append(newInterval)

        return occurancy

    #order Array from high to low, if index is passed sorte [[]] in order of given index
    def order(self, M, index = 0):
        if index >= len(M[0]) or index < 0:
            return 0
        else:
            for i in range(len(M)-1, 0, -1):
                for j in range(i):
                    if M[j][index] < M[j+1][index]:
                        temp = M[j]
                        M[j] = M[j+1]
                        M[j+1] = temp
            return M

    def printMatrix(self, M):
        for el in M:
            element = ''
            for e in el:
                element = element + str(e) + '\t'
            print(element)

    def writeMatrix(self, M,  fileName):
        try:
            with open(fileName, 'a') as f:
                for el in M:
                    for i in range(0, len(el)):
                        if i==len(el)-1:
                            f.write(str(el[i])+'\n')
                        else:
                            f.write(str(el[i])+';')
            return 1

        except IOError:
            print("error while writting to a file")
            return 0

    def returnDevices(self):
        return self.devicesList
