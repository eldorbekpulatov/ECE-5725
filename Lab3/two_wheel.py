import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library
import os

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering

'''
###########INTERNAL###############
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
def GPIO17_callback(channel):
    print("falling edge detected on 17")
    
def GPIO22_callback(channel):
    print("falling edge detected on 22")
    
def GPIO23_callback(channel):
    print("falling edge detected on 23")
    
def GPIO27_callback(channel):
    print("falling edge detected on 27")
    
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=200)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=200)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=200)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)
'''


###########EXTERNAL###############
# Pin 21 - LLL ==> Left, Clockwise
# Pin 16 - LL  ==> Left, Stop
# Pin 12 - L   ==> Left, Counter-Clockwise
GPIO.setup(21, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(12, GPIO.IN)

# Pin 20 - R   ==> Right, Counter-Clockwise
# Pin 25 - RR  ==> Right, Stop
# Pin 24 - RRR ==> Right, Clockwise
GPIO.setup(20, GPIO.IN)
GPIO.setup(25, GPIO.IN)
GPIO.setup(24, GPIO.IN)

def GPIO21_callback(channel):
    print("falling edge detected on 21")

def GPIO16_callback(channel):
    print("falling edge detected on 16")
    
def GPIO12_callback(channel):
    print("falling edge detected on 12")
    
def GPIO20_callback(channel):
    print("falling edge detected on 20")

def GPIO25_callback(channel):
    print("falling edge detected on 25")
    
def GPIO24_callback(channel):
    print("falling edge detected on 24")
    
GPIO.add_event_detect(21, GPIO.FALLING, callback=GPIO21_callback, bouncetime=200)
GPIO.add_event_detect(16, GPIO.FALLING, callback=GPIO16_callback, bouncetime=200)
GPIO.add_event_detect(12, GPIO.FALLING, callback=GPIO12_callback, bouncetime=200)

GPIO.add_event_detect(20, GPIO.FALLING, callback=GPIO20_callback, bouncetime=200)
GPIO.add_event_detect(25, GPIO.FALLING, callback=GPIO25_callback, bouncetime=200)
GPIO.add_event_detect(24, GPIO.FALLING, callback=GPIO24_callback, bouncetime=200)

#####################SERVOS######################
#GPIO.setup(26, GPIO.OUT)
#GPIO.setup(19, GPIO.OUT)


def calculateFreqDC(step):
    w = (1.5 + step)
    d = (20+w)
    return (1000/d, w/d*100)

def setMode(step):
    (fq, dc) = calculateFreqDC(step)    
    pwm.ChangeDutyCycle(dc)      
    pwm.ChangeFrequency(fq)
    
try:
    #(fq, dc) = calculateFreqDC(0)                 
    #pwm = GPIO.PWM(pwmPin, fq)      # Initialize PWM on pwmPin
    #pwm.start(dc)                   # Start PWM
    GPIO.wait_for_edge(20, GPIO.FALLING)
    
    
except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit

GPIO.cleanup() # clean up GPIO on normal exit




