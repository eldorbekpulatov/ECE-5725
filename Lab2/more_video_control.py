import RPi.GPIO as GPIO
import time
import os

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...

# Pin 17 - pause
# Pin 19 - FF 30
# Pin 22 - FF 10
# Pin 23 - RW 10
# Pin 26 - RW 30
# Pin 27 - quit
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN)
GPIO.setup(26, GPIO.IN)

pressed = False

while True:
    time.sleep(0.2)  # Without sleep, no screen output!
    if ( not GPIO.input(17) ):
        os.system('echo "pause" > $(pwd)/video_fifo')
    elif ( not GPIO.input(19) ):
        os.system('echo "seek 30" > $(pwd)/video_fifo')
    elif ( not GPIO.input(26) ):
        os.system('echo "seek -30" > $(pwd)/video_fifo')
    elif ( not GPIO.input(22) ):
        os.system('echo "seek 10" > $(pwd)/video_fifo')
    elif ( not GPIO.input(23) ):
        os.system('echo "seek -10" > $(pwd)/video_fifo')
    elif ( not GPIO.input(27) ):
        os.system('echo "quit" > $(pwd)/video_fifo')
        break
    

