import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library

 
GPIO.setmode(GPIO.BCM)    # Set Pi to use pin number when referencing GPIO pins.
                          # Can use GPIO.setmode(GPIO.BCM) instead to use 
                          # Broadcom SOC channel names.

pwmPin = 26                     # set pin number
fq = 1000/21.5                  # set te frequency
dc = 150/21.5                   # set the duty cycle

GPIO.setup(pwmPin, GPIO.OUT)    # Set GPIO pin to output mode
pwm = GPIO.PWM(pwmPin, fq)      # Initialize PWM on pwmPin
pwm.start(dc)                   # Start PWM 
 
try:
    while(True):
        pass
except:
    pwm.stop()                      # stop PWM
    pass

GPIO.cleanup()                  # clean up GPIO



