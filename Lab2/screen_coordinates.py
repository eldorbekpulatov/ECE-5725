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
#pygame.mouse.set_visible(False)


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
size = width, height = (320, 240)
screen = pygame.display.set_mode(size)

# window title 
pygame.display.set_caption("screen_coordinates")

# Font and size
font = pygame.font.Font(None, 30)

# list of buttons : positions
buttons= { "quit": (80, 220), "start": (220, 220) }
 

try: 
    # Set the screen background
    screen.fill(BLACK)
    for text, pos in buttons.items():
        text_surface= font.render(text, True, WHITE)
        rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, rect)
    pygame.display.flip()

    # Open the file to store coordinate clicks
    click_file = open("Click_Coords.txt","w+")
        
    # ------main loop-------
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break
            elif(event.type is MOUSEBUTTONUP):
                x,y = pygame.mouse.get_pos()
                coord_str = "x = " + str(x) + ", y = "+ str(y) + "\n"
                print(coord_str)
                click_file.write(coord_str)
                
                if (y > 200) and (x > 50 and x < 110):
                    playing = False
                    break
                else:
                    screen.fill(BLACK)
                    for text, pos in buttons.items():
                        text_surface= font.render(text, True, WHITE)
                        rect = text_surface.get_rect(center=pos)
                        screen.blit(text_surface, rect)
                    
                    text_surface= font.render("Hit at ({}, {})".format(x,y), True, WHITE)
                    rect = text_surface.get_rect(center=(160,110))
                    screen.blit(text_surface, rect)
                    
                    pygame.display.flip()
       
except KeyboardInterrupt:
    # clean up GPIO, close txt file, and quit pygame on CTRL+C exit 
    click_file.close()
    GPIO.cleanup() 
    pygame.quit()

# clean up GPIO, close txt file, and quit pygame on normal exit
click_file.close()
GPIO.cleanup() 
pygame.quit()

