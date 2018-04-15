import cv2
import sys
import numpy as np
# import copy
# import math
# import time

X = 300
Y = 300
TRASHOLD = 30
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
height, width, channels = frame.shape

cv2.namedWindow('video', cv2.WINDOW_AUTOSIZE )
cv2.setWindowProperty('video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

print("HEIGHT: ", height, "\nWIDTH: ", width, "\nCHANNELS: ", channels)

while True:
    ret, frame  = cap.read()
    px = frame[X, Y]
    lB     = "B: " + str(px[0])
    lG     = "G: " + str(px[1])
    lR     = "R: " + str(px[2])
    lA     = "A: " + str(int(np.mean(px)))


    cv2.rectangle(frame, (5, 5), (60, 75), (242, 242, 242), -1)
    cv2.rectangle(frame, (5, 5), (60, 75), (50, 50, 50),     1)

    cv2.putText(frame, lB, (15,20), font, 0.35, (255,0,0), 1, cv2.LINE_AA)
    cv2.putText(frame, lG, (15,35), font, 0.35, (0,255,0), 1, cv2.LINE_AA)
    cv2.putText(frame, lR, (15,50), font, 0.35, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(frame, lA, (15,65), font, 0.35, (0,0,0),   1, cv2.LINE_AA)

    cv2.rectangle( frame, (X-3, Y-3), (X+3, Y+3), (0, 0, 255), -1)
    cv2.line(   frame, (0, Y), (width, Y),  (0, 0, 255), 1)
    cv2.line(   frame, (X, 0), (X, height), (0, 0, 255), 1)

    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
