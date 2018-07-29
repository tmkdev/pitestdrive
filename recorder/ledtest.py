import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

green1=17
red=22


for led in [17,22,23,24]:
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, False)
