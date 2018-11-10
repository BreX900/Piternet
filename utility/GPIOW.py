import logging.config

class GPIO:
    log = logging.getLogger(__name__)


    pins = []
    boardPins = {0:0,1:0,2:True,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:1,20:0}
    BCM = 1
    OUT = 2
    IN = 3
    @staticmethod
    def setwarnings(boolean):
        return

    @staticmethod
    def setmode(mode):
        return

    @staticmethod
    def setup(pin, mode):
        if not GPIO.pins.__contains__(pin):
            GPIO.pins.append(pin)

    @staticmethod
    def output(pin, tension):
        #GPIO.log.info("GPIOW - StatusBoard: " + str(GPIO.boardPins) + "\nPins: " + str(GPIO.pins))
        if GPIO.pins.__contains__(pin):
            GPIO.boardPins[pin] = tension

    @staticmethod
    def input(pin):
        #GPIO.log.info("GPIOW - StatusBoard: " + str(GPIO.boardPins) + "\nPins: " + str(GPIO.pins))
        return GPIO.boardPins[pin]

    @staticmethod
    def cleanup():
        for pin in GPIO.pins:
            GPIO.boardPins[pin] = 0
        GPIO.pins = []

