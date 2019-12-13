import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library
import pygame


# initilize
GPIO.setmode(GPIO.BCM)
pygame.mixer.init()


# set pin numbers
LaserPin = 16
MotorPin = 12
TriggerPin = 20
ReloadPin = 21
SensorPin = 13
GreenPin = 19
RedPin = 26


# Set GPIO pin modes
GPIO.setup(LaserPin, GPIO.OUT)
GPIO.setup(MotorPin, GPIO.OUT)
GPIO.setup(RedPin, GPIO.OUT)
GPIO.setup(GreenPin, GPIO.OUT)

GPIO.setup(SensorPin, GPIO.IN)
GPIO.setup(TriggerPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ReloadPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def reload_callback(channel):
    print("reload pressed")
    pygame.mixer.music.load("reload.mp3")
    pygame.mixer.music.play()


def trigger_callback(channel):
    if not GPIO.input(TriggerPin):
        print("pressed")
        pygame.mixer.music.load("shot.mp3")
        pygame.mixer.music.play() # make it a thread
        GPIO.output(LaserPin, GPIO.HIGH)
        GPIO.output(MotorPin, GPIO.HIGH)
    else:
        print("released")
        GPIO.output(LaserPin, GPIO.LOW)
        GPIO.output(MotorPin, GPIO.LOW)
    

def sensor_callback(channel):
    if GPIO.input(TriggerPin):
        print("light detected")
        GPIO.output(RedPin, GPIO.HIGH)
        GPIO.output(GreenPin, GPIO.LOW)
    else:
        GPIO.output(RedPin, GPIO.LOW)
        GPIO.output(GreenPin, GPIO.HIGH)
    
GPIO.add_event_detect(TriggerPin, GPIO.BOTH, callback=trigger_callback, bouncetime=10)
GPIO.add_event_detect(SensorPin, GPIO.BOTH, callback=sensor_callback, bouncetime=10)
GPIO.add_event_detect(ReloadPin, GPIO.FALLING, callback=reload_callback, bouncetime=200)


try:
    while True:
        pass

except:
    pass

GPIO.cleanup()                  # clean up GPIO
