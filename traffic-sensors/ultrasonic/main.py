import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)

try:
    while True:
        GPIO.output(7, True)
        time.sleep(2)
        GPIO.output(7, False)
        time.sleep(2)

except KeyboardInterrupt:
    print("Program exited by user on event KeyboardInterrupt")
