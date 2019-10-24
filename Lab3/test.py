import RPi.GPIO as GPIO
import subprocess
import time


GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...

# Pin 17 - pause
# Pin 22 - FF 10
# Pin 23 - RW 10
# Pin 19 - FF 30
# Pin 26 - RW 30
# Pin 27 - quit
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    
def GPIO17_callback(channel):
    print("falling edge detected on 17")
    
def GPIO22_callback(channel):
    print("falling edge detected on 22")
      
def GPIO23_callback(channel):
    print("falling edge detected on 23")
    
    

#GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=200)
#GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=200)
#GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=200)



try:
    print("Waiting for falling edge on port 27")
    GPIO.wait_for_edge(27, GPIO.FALLING)
    print("pressed 27")
    
    
except:
    pass
    

GPIO.cleanup() # clean up GPIO on normal exit
