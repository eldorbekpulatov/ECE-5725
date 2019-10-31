import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library

 
GPIO.setmode(GPIO.BCM)    # Set Pi to use pin number when referencing GPIO pins.
                          # Can use GPIO.setmode(GPIO.BCM) instead to use 
                          # Broadcom SOC channel names.

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # QUIT
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # FREQ MULT

running = True

fq = 100                         # set frequency to 10 Hz
half_T = 0.5/fq                 # pulse is high or low for half the period

def GPIO27_callback(channel):
    global running
    running = False
    
def GPIO23_callback(channel):
    global fq
    global half_T
    fq += 100
    half_T = 0.5/fq  


GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=200)

LEDpin = 13                     # set pin number to 26
GPIO.setup(LEDpin, GPIO.OUT)    # Set GPIO pin 26 to output mode.


try:
    while running:
        GPIO.output(LEDpin, GPIO.LOW)
        time.sleep(half_T)
        GPIO.output(LEDpin, GPIO.HIGH)
        time.sleep(half_T)
    
except:
    pass
    
# clean up GPIO and quit pygame on normal exit
GPIO.cleanup() 
