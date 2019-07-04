import RPi.GPIO as GPIO
import time
 
class led:
    def __init__(self):
        print("FIXME: Constructor")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18,GPIO.OUT)
    def turn_on(self):
        print("FIXME: Turn on light")
        GPIO.output(18,GPIO.HIGH)
    def turn_off(self):
        print("FIXME: Turn off light")
        GPIO.output(18,GPIO.LOW)
