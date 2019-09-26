import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2)  # Without sleep, no screen output!
    if ( not GPIO.input(17) ):
        print "Button 17 pressed...."
