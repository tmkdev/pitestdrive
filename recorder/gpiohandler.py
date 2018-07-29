import RPi.GPIO as GPIO
import logging

class GpioHandler(object):
    green1=17
    red=22
    green2=23
    green3=24
    all_leds = [ green1, red, green2, green3 ]

    switch=26

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch, GPIO.IN)

        for led in self.all_leds:
            GPIO.setup(led, GPIO.OUT)
            GPIO.output(led, False)

    def set_all(self, ledstate):
         for led in self.all_leds:
            GPIO.output(led, ledstate)

    def set_led(self, led):
        GPIO.output(led, True)

    def clear_led(sel, led):
        GPIO.output(led, False)






