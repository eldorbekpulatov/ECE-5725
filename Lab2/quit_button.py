import os
import sys
import time
import pygame
import subprocess
from pygame.locals import * 
from utils import *
import RPi.GPIO as GPIO

os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# variable used to break out of the loop
playing = True  

def GPIO27_callback(channel):
    global playing
    playing = False

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pin 27 - quit 
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)

pygame.init()

#make mouse invisible
pygame.mouse.set_visible(False)


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
size = width, height = (320, 240)
screen = pygame.display.set_mode(size)

# window title 
pygame.display.set_caption("quit_button")

# Font and size
font = pygame.font.Font(None, 50)

# list of buttons : positions
buttons= { "quit": (80,180) }
 

try: 
    # Set the screen background
    screen.fill(BLACK)
    for text, pos in buttons.items():
        text_surface= font.render(text, True, WHITE)
        rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, rect)
    pygame.display.flip()
        
    # ------main loop-------
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break
            elif(event.type is MOUSEBUTTONUP):
                playing = False
                break
       
except KeyboardInterrupt:
    # clean up GPIO and quit pygame on CTRL+C exit 
    GPIO.cleanup() 
    pygame.quit()

# clean up GPIO and quit pygame on normal exit
GPIO.cleanup() 
pygame.quit()

