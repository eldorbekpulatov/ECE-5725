import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN)
GPIO.setup(26, GPIO.IN)

while True:
    time.sleep(0.2)  # Without sleep, no screen output!
    if ( not GPIO.input(17) ):
        print "Button 17 pressed...."
    if ( not GPIO.input(22) ):
        print "Button 22 pressed...."
    if ( not GPIO.input(23) ):
        print "Button 23 pressed...."   
    if ( not GPIO.input(19) ):
        print "Button 19 pressed...."    
    if ( not GPIO.input(26) ):
        print "Button 26 pressed...."
    if ( not GPIO.input(27) ):
        print "Button 27 pressed...."
        break

