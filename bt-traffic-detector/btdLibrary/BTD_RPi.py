import RPi.GPIO as GPIO


class RPi:
    CATCHED = False

    def __init__(self, RPI_START_MEASURE, RPI_EXIT, RPI_READY, RPI_RUN, RPI_CATCHED):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.RPI_START_MEASURE = RPI_START_MEASURE
        GPIO.setup(self.RPI_START_MEASURE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.RPI_EXIT = RPI_EXIT
        GPIO.setup(self.RPI_EXIT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.RPI_READY = RPI_READY
        GPIO.setup(self.RPI_READY, GPIO.OUT)

        self.RPI_RUN = RPI_RUN
        GPIO.setup(self.RPI_RUN, GPIO.OUT)

        self.RPI_CATCHED = RPI_CATCHED
        GPIO.setup(self.RPI_CATCHED, GPIO.OUT)

        self.RPiReady()

    def __del__(self):
            print("CLEANING GPIO")
            if GPIO: GPIO.cleanup()


    def Power(self):
        return GPIO.input(self.RPI_EXIT)

    def Measure(self):
        return GPIO.input(self.RPI_START_MEASURE)

    def RPiReady(self):
        GPIO.output(self.RPI_READY, True)

    def btdRunning(self, ON):
        GPIO.output(self.RPI_RUN, ON)

    def catched(self):
        if self.CATCHED:
            GPIO.output(self.RPI_CATCHED, False)
            self.CATCHED = False
        else:
            GPIO.output(self.RPI_CATCHED, True)
            self.CATCHED = True
