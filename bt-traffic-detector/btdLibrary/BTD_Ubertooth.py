import os
import time
import re
from sys import exit

class Ubertooth:
	ALREADY_LOADED_LAP = []
	START_TIME = 0
	WAIT_TIME = 10
	FILE_NAME = ""

	def __init__(self, START_TIME, CWD, FILE_NAME_GROUP, WAIT_TIME):
		self.START_TIME = START_TIME
		self.FILE_NAME = self.newFile(CWD, FILE_NAME_GROUP)
		self.WAIT_TIME = WAIT_TIME

		startTimeFormated = 'start time: [{}]'.format(self.formatTime(START_TIME))
		print("Starting at:\t[", startTimeFormated, ']')
		print("Save to dir: \t", self.FILE_NAME, '\n\n')

		self.writeToFile(self.FILE_NAME, startTimeFormated)

    # function format time in hh:mm:ss
	def formatTime(self, T):
		s = '{}:{}:{}'.format(int(((T/3600)%24)+1), int((T/60)%60), int((T)%60))
		return s

	#find free smallest fileName and return this name
	def newFile(self, dirPath, filesGroup):
		dirPath = str(dirPath)
		filesGroup = str(filesGroup)
		biggestInDir = 0
		smallestFreeInDir = 0
		NewFileName = ''

        # check if dir path ends with "/"
		if not dirPath.endswith("/"):
			dirPath = dirPath + "/"

        # of path doesn't exists create it
		if not os.path.exists(dirPath):
			os.makedirs(dirPath)

		for file in os.listdir(dirPath):
			if file.endswith('.txt') and file.startswith(filesGroup):
				fileNumb = file[len(filesGroup):-4]
				try:	#check if string represent int number
					int(fileNumb)
					if biggestInDir < int(fileNumb):
						biggestInDir = int(fileNumb)
				except ValueError:
					print("Problem with filename")

		smallestFreeInDir = biggestInDir+1
		NewFileName = filesGroup + str(smallestFreeInDir) + '.txt'
		return dirPath+NewFileName

	#take filePath, open file and write thingToWrite
	def writeToFile(self, filePath, stringToWrite):
		filePath = str(filePath)
		stringToWrite = str(stringToWrite)
		try:
			with open(filePath, 'a') as f:	#open file and close it no matter how nested code exit
				f.write(stringToWrite + "\n")
		except IOError:
			print("unable to open file for writting")
			exit()

	# take line and return list of parameters [systime, LAP]
	def devPar(self, ln):
		ln = ln.decode(encoding="utf-8")
		ln = ln.split(' ')
		for col in ln:
			if re.match(r'^systime', col):
				systime = col
			elif re.match(r'^LAP', col):
				LAP = col
		try:
			systime = int(systime.split('=')[1])
			LAP 	= LAP.split('=')[1]
			return [LAP, systime]
		except:
			print("There seems to be an error with Ubertooth, try to unmount it and mount again, if it won't help, restart compuret")
			exit()

    # check if device was already readed in time interval WAIT_TIME
    # return 0 if
	def isWaiting(self, device):
		isWaiting = False
		if self.ALREADY_LOADED_LAP:	#if array is not empty
			#remove from array all expired elements
			for el in self.ALREADY_LOADED_LAP:
				# print(el[0], " ", el[1], " -> ", device[0], " ", device[1])

				if el[1] + self.WAIT_TIME <= device[1]:
					self.ALREADY_LOADED_LAP.remove(el)
					continue

			#check if is contained in ALREADY_LOADED_LAP
			for el in self.ALREADY_LOADED_LAP:
				if device[0] == el[0]:
					isWaiting = True

		# if not in list, write it down
		if not isWaiting:
			self.ALREADY_LOADED_LAP.append([device[0], device[1]])
		return isWaiting

    # Get line readed from Ubertooth, return True if line was accepted and readed to file
    # Return False in case of nonvalid line or if device was detected in time interval
	def getLine(self, ln):
		if len(ln) < 50:	# in case of wrong line (Uberooth after few catched packages read other parts of address and return it)
			return False

		#get parameters from whole line
		device = self.devPar(ln)
		if not self.isWaiting(device):
			stringToWrite = '{} {}'.format(device[0], self.formatTime(device[1]))
			print(stringToWrite)
			self.writeToFile(self.FILE_NAME, stringToWrite)
			return True

		return False
