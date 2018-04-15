import MeasureC


# CREATE OBJECT
set1 = MeasureC.Measurement("data/M1.txt")
set1.printPar()

# PARAMETERS
time = set1.retTime()
position = set1.retPosition()
speed = set1.retSpeed()

# max speed
maxSpeed = set1.maxSpeed()
print ("\nMAX SPEED:")
print(maxSpeed)


# location of trigger points
triggers = set1.triggerArea()
print ("\nTRIGGERS ARE: ")
for i in range(0, len(triggers)):
	print("%d. trigger is located at coordinates: [ %.2f, %.2f]" % ((i+1), triggers[i][0], triggers[i][1] ) )

# Brake and Throttle arround trigger
BrThArroundTrigger = set1.BrThArroundTrigger(1)
print("\nBAKE AND THROTTLE IN AREA OF 2ND TRIGGER CODE: (print just few)")
for i in range(20,25):
	print(BrThArroundTrigger[i])
print("\nfirst time: ", BrThArroundTrigger[0][0], "\nlast time: ", BrThArroundTrigger[len(BrThArroundTrigger)-1][0])

# average between triggers
averageBetweenTriggers = set1.averageBetweenTriggers()
print("\nPATH AND AVERAGE SPEED BETWEEN FIRST AND LAST TRIGGER: ")
print("time between triggers: 			", averageBetweenTriggers[0], "[h]")
print("average speed between triggers is: 	", averageBetweenTriggers[1], "[km/h]")

# PLOTS
set1.plotSpeed()
set1.plotPosTriggers()
set1.plotBrThArroundTriggers(0)
set1.plotBrThArroundTriggers(1)
set1.plotBrThArroundTriggers(2)
