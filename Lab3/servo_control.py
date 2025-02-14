import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library


def calculateFreqDC(step):
    """
    Returns the (frequency, dutyCycle) as tuple given a step.
    
    Param: step (float) bounded by -0.2 <= step <= +0.2
    Return: (freq, dutyCycle) tuple of floats
    """
    w = (1.5 + step)
    d = (20+w)
    return (1000/d, w/d*100)

def setMode(step,pwm):
    (fq, dc) = calculateFreqDC(step)    
    pwm.ChangeDutyCycle(dc)      
    pwm.ChangeFrequency(fq)
    
 
GPIO.setmode(GPIO.BCM)    # Set Pi to use pin number when referencing GPIO pins.
                          # Can use GPIO.setmode(GPIO.BCM) instead to use 
                          # Broadcom SOC channel names.

pwmPin = 26
GPIO.setup(pwmPin, GPIO.OUT)    # Set GPIO pin to output mode# set pin number


try:
    
    (fq, dc) = calculateFreqDC(0)                 
    pwm = GPIO.PWM(pwmPin, fq)      # Initialize PWM on pwmPin
    pwm.start(dc)                   # Start PWM
    
    # speed up Clockwise
    for step in range(0, 21, 2):
        step = step/100.0
        setMode(step,pwm)
        time.sleep(3)

    #speed up ounter-clockwise
    for step in range(0, -21, -2):
        step = step/100.0
        setMode(step,pwm)
        time.sleep(3)

    pwm.stop()                      # stop PWM
    
except:
    pass

GPIO.cleanup()                  # clean up GPIO



