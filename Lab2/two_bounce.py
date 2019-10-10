import os
import sys
import time
import pygame
import subprocess
from pygame.locals import * 
import RPi.GPIO as GPIO

start = time.time()

os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# variable used to break out of pygame loop
playing = True 

def GPIO27_callback(channel):
    global playing
    playing = False
    
GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pin 27 - quit 
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)

# --------------PYGAME-----------------
# initialize the game
pygame.init()

# make pointer invisible
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
pygame.display.set_caption("two_bounce")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# ball parameters
balls = [
    {
        "path_to_img": "magic_ball.png",
        "pos" : [50, 50],
        "dim" : [100, 100],
        "rad" : [50, 50],
        "vel" : [5, 5],
        "img" : None
    },
    {
        "path_to_img": "soccer_ball.png",
        "pos" : [100, 100],
        "dim" : [100, 100],
        "rad" : [50, 50],
        "vel" : [3, 3],
        "img" : None
    }
]

def calculate(balls):
    # for each ball
    for ball in balls:
        # collide left and right walls
        if (ball["pos"][0] + ball["dim"][0] > width) or (ball["pos"][0] < 0):
            ball["vel"][0] = -1*ball["vel"][0]
        
        # collide up and down walls
        if (ball["pos"][1] + ball["dim"][1]> height) or (ball["pos"][1] < 0):
            ball["vel"][1] = -1*ball["vel"][1]
        
        # update positions
        ball["pos"][0] += ball["vel"][0]
        ball["pos"][1] += ball["vel"][1]
         
try: 
    # load and scale the balls
    for ball in balls:
        img = pygame.image.load(ball["path_to_img"])
        ball["img"] = pygame.transform.scale(img, ball["dim"])
    
    # ------main loop-------
    while (playing and (time.time() - start < 30)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break
            
        # Set the screen background
        screen.fill(GREEN)
        
        # calculate trajectories
        calculate(balls)

        # for each ball
        for ball in balls:
            # Draw the ball
            screen.blit(ball["img"], ball["pos"])

        # update the screen
        pygame.display.flip()
 
        # Limit to 30 frames per second
        clock.tick(60)
        
       
except KeyboardInterrupt:
    # clean up GPIO and quit pygame on CTRL+C exit 
    GPIO.cleanup() 
    pygame.quit()

# clean up GPIO and quit pygame on normal exit
GPIO.cleanup() 
pygame.quit()

