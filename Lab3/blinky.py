import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library

 
GPIO.setmode(GPIO.BCM)    # Set Pi to use pin number when referencing GPIO pins.
                          # Can use GPIO.setmode(GPIO.BCM) instead to use 
                          # Broadcom SOC channel names.

pwmPin = 26                     # set pin number to 26
GPIO.setup(pwmPin, GPIO.OUT)    # Set GPIO pin 26 to output mode.

fq = 10                         # set frequency to 30 Hz
dc = 50                         # set dc variable to 50 for 50%
pwm = GPIO.PWM(pwmPin, fq)      # Initialize PWM on pwmPin 100Hz frequency


try:
    pwm.start(dc)                   # Start PWM with 0% duty cycle
    time.sleep(5)                   # sleep for 5 seconds

    fq = 5
    dc = 25 
    pwm.ChangeDutyCycle(dc)         # where 0.0 <= dc <= 100.0
    pwm.ChangeFrequency(fq)         # where freq is the new frequency in Hz

    time.sleep(5)                   # sleep for 5 seconds
    pwm.stop()                      # stop PWM
    
except:
    pass
    
# clean up GPIO and quit pygame on normal exit
GPIO.cleanup() 

