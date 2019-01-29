from utility.pattern import Singleton
from utility.development import DEVELOPMENT
from utility.system import system, System

if system == System.WINDOWS:
    from utility.GPIOW import GPIO
else:
    import RPi.GPIO as GPIO


class Board(metaclass=Singleton):  # GPIO.setwarnings(False)
    HIGH = 0  # ON
    LOW = 1  # OFF

    _pins = None

    @staticmethod
    def _newPin(*pins):
        if Board._pins is None:
            Board._pins = {}
            GPIO.setmode(GPIO.BCM)
        for pin in pins:
            if not Board._pins.__contains__(pin):
                GPIO.setup(pin, GPIO.OUT)
                Board._pins[pin] = 1
    @staticmethod
    def signal(pin):
        Board._newPin(pin)
        return GPIO.input(pin)
    @staticmethod
    def info():
        string = ""
        for pin in Board._pins:
            string += "Pin"+str(pin) + ":" + ("ON" if Board.signal(pin)==Board.HIGH else 'OFF') + " | "
        return string[:-3]
    @staticmethod
    def output(pin, tension):
        Board._newPin(pin)
        return GPIO.output(pin, tension)
    @staticmethod
    def reset(check=True):
        log = "Board.reset("+str(check)+")"
        if Board._pins:
            log += ": "
            for pin in Board._pins:
                tension = GPIO.input(pin)
                log += str(pin)+":" + str(tension)
                if not tension:
                    Board.output(pin, Board.LOW)
                    log += "R"
                log += "-"
            GPIO.cleanup()
        Board._pins = {}
        return log

    @staticmethod
    def resetAll(check=True):
        log = "Board.resetAll("+str(check)+"): "
        GPIO.setmode(GPIO.BCM)
        for pin in range(1, 21):
            GPIO.setup(pin, GPIO.OUT)
            log += str(pin)
            if check:
                tension = GPIO.input(pin)
                log += ":"+str(tension)
                if not tension:
                    GPIO.output(pin, Board.LOW)
                    log += "R"
            log += "-"
        GPIO.cleanup()
        return log[0:-1]