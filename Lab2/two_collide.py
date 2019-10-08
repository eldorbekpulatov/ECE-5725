import RPi.GPIO as GPIO
import subprocess
import time
import sys
import os
import pygame
from pygame.locals import *   # for event MOUSE variables

os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

playing = True  # variable used to break out of the loop
def GPIO27_callback(channel):
    global playing
    playing = False
GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pin 27 - quit 
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)


###########################################################
#########################PYGAME############################

pygame.init()
pygame.mouse.set_visible(False) # make pointer invisible

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
size = width, height = (320, 240)
screen = pygame.display.set_mode(size)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# window title 
pygame.display.set_caption("two_bounce")

path_to_image_1 = "magic_ball.png"
path_to_image_2 = "soccer_ball.png"


# Starting positions
surf_x_1 = 50
surf_y_1 = 50

surf_x_2 = 100
surf_y_2 = 100
 
# Speed and direction of rectangle
delta_x_1 = 5
delta_y_1 = 5

delta_x_2 = 3
delta_y_2 = 3

# image sizes
size_x_1 = 100
size_y_1 = 100

size_x_2 = 100
size_y_2 = 100

# load the images
image_1 = pygame.image.load(path_to_image_1)
image_2 = pygame.image.load(path_to_image_2)

# scale one of the balls
image_1 = pygame.transform.scale(image_1, (size_x_1, size_y_1))
image_2 = pygame.transform.scale(image_2, (size_x_2, size_y_2))

try:
    # -------- Main Program Loop -----------
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break
            
        # Set the screen background
        screen.fill(GREEN)
        
        # Draw the ball
        screen.blit(image_1, (surf_x_1, surf_y_1))
        screen.blit(image_2, (surf_x_2, surf_y_2))
        
        # update the screen
        pygame.display.flip()
 
        # Limit to 30 frames per second
        clock.tick(60)
        
        
        # Move the rectangle starting point
        if (surf_x_1 + size_x_1 > width) or (surf_x_1 < 0):
            delta_x_1 = -1*delta_x_1
        if (surf_y_1 + size_y_1 > height) or (surf_y_1 < 0):
            delta_y_1 = -1*delta_y_1
            
        if (surf_x_2 + size_x_2 > width) or (surf_x_2 < 0):
            delta_x_2 = -1*delta_x_2
        if (surf_y_2 + size_y_2 > height) or (surf_y_2 < 0):
            delta_y_2 = -1*delta_y_2
    
        surf_x_1 += delta_x_1
        surf_y_1 += delta_y_1
        
        surf_x_2 += delta_x_2
        surf_y_2 += delta_y_2
        
       
except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
    pygame.quit()

GPIO.cleanup() # clean up GPIO on normal exit
pygame.quit()

