import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library
import os


def calculateFreqDC(step):
    w, d = (1.5 + step), (20+w)
    return (1000/d, w/d*100)

def setMode(step, pwm):
    (fq, dc) = calculateFreqDC(step)    
    pwm.ChangeDutyCycle(dc)      
    pwm.ChangeFrequency(fq)

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering

###########EXTERNAL###############
# Pin 21 - LLL ==> Left, Clockwise
# Pin 16 - LL  ==> Left, Stop
# Pin 12 - L   ==> Left, Counter-Clockwise
GPIO.setup(21, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(12, GPIO.IN)

# Pin 20 - R   ==> Right, Counter-Clockwise
# Pin 5  - RR  ==> Right, Stop
# Pin 4  - RRR ==> Right, Clockwise
GPIO.setup(20, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(4, GPIO.IN)

def GPIO21_callback(channel):
    print("falling edge detected on 21")
    setMode(-0.2, pwmL)
    
def GPIO16_callback(channel):
    print("falling edge detected on 16")
    setMode(0, pwmL)
    
def GPIO12_callback(channel):
    print("falling edge detected on 12")
    setMode(0.2, pwmL)
    
def GPIO20_callback(channel):
    print("falling edge detected on 20")
    setMode(-0.2, pwmR)

def GPIO5_callback(channel):
    print("falling edge detected on 5")
    setMode(0, pwmR)
    
def GPIO4_callback(channel):
    print("falling edge detected on 4")
    setMode(0.2, pwmR)

GPIO.add_event_detect(21, GPIO.FALLING, callback=GPIO21_callback, bouncetime=200)
GPIO.add_event_detect(16, GPIO.FALLING, callback=GPIO16_callback, bouncetime=200)
GPIO.add_event_detect(12, GPIO.FALLING, callback=GPIO12_callback, bouncetime=200)

GPIO.add_event_detect(20, GPIO.FALLING, callback=GPIO20_callback, bouncetime=200)
GPIO.add_event_detect(5, GPIO.FALLING, callback=GPIO5_callback, bouncetime=200)
GPIO.add_event_detect(4, GPIO.FALLING, callback=GPIO4_callback, bouncetime=200)


#####################SERVOS######################
GPIO.setup(26, GPIO.OUT) # LEFT
GPIO.setup(19, GPIO.OUT) # RIGHT
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # QUIT

(fq, dc) = calculateFreqDC(0)                  
pwmL = GPIO.PWM(26, fq)          # Intialize PWM
pwmR = GPIO.PWM(19, fq)          # Intialize PWM
try:
    pwmL.start(dc)                   # Start PWM
    pwmR.start(dc)                   # Start PWM
    GPIO.wait_for_edge(27, GPIO.FALLING) # wait for quit
    pwmL.stop()
    pwmR.stop()
    
except:
    pass
GPIO.cleanup() # clean up GPIO on exit

