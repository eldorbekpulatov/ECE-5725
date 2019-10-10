import os
import sys
import time
import pygame
import subprocess
from pygame.locals import * 
from utils import *
import RPi.GPIO as GPIO

#os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
#os.putenv('SDL_FBDEV', '/dev/fb1')     
#os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# variable used to break out of the loop
playing = True    # quit hasn't been pressed 
animating = False # start hasn't been pressed

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
pygame.display.set_caption("two_button")

# Font and size
font = pygame.font.Font(None, 30)

# list of buttons : positions
buttons= { "quit": (80, 220), "start": (220, 220) }
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Controls coordinate messages
coord= ""
coord_time = time.time() - 2
coord_pos = (160, 200)

# ball parameters
balls = [
    {
        "path_to_img": "magic_ball.png",
        "pos" : [0, 0],
        "dim" : [100, 100],
        "rad" : [50, 50],
        "vel" : [1, 1],
        "img" : None
    },
    {
        "path_to_img": "soccer_ball.png",
        "pos" : [220, 140],
        "dim" : [100, 100],
        "rad" : [50, 50],
        "vel" : [1, 1],
        "img" : None
    }
]

def calculate(balls):
    delr = vector_sub(balls[0]["pos"], balls[1]["pos"])
    if (vector_mag_sq(delr) <= (100**2)):
        delv = vector_sub(balls[0]["vel"], balls[1]["vel"])
        delta = vector_del(delv, delr)

        balls[0]['vel'] = vector_add(balls[0]['vel'], delta)
        balls[1]['vel'] = vector_sub(balls[1]['vel'], delta)

    # for each ball
    for ball in balls:
        # check collide left and right walls
        if (ball["pos"][0] + ball["dim"][0] > width) or (ball["pos"][0] < 0):
            ball["vel"][0] = -1*ball["vel"][0]
        
        # check collide up and down walls
        if (ball["pos"][1] + ball["dim"][1]> height) or (ball["pos"][1] < 0):
            ball["vel"][1] = -1*ball["vel"][1]

        # update positions
        ball["pos"] = vector_add(ball["pos"], ball["vel"])
        
try: 
    # Set the screen background
#    screen.fill(BLACK)
#    for text, pos in buttons.items():
#        text_surface= font.render(text, True, WHITE)
#        rect = text_surface.get_rect(center=pos)
#        screen.blit(text_surface, rect)
#    pygame.display.flip()
        
    # ------main loop-------
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                animating = False
                playing = False
                break
            elif(event.type is MOUSEBUTTONUP):
                x,y = pygame.mouse.get_pos()
                
                if (y > 200) and (x > 50 and x < 110):
                    animating = False
                    playing = False
                    break
                elif (y > 200) and (x > 190 and x < 250):
                    animating = True
                else:
                    coord = "x = " + str(x) + ", y = "+ str(y)
                    coord_time = time.time()
        if animating:
             # load and scale the balls
            for ball in balls:
                img = pygame.image.load(ball["path_to_img"])
                ball["img"] = pygame.transform.scale(img, ball["dim"])
            
            # Set the screen background
            screen.fill(GREEN)
            
            # calculate trajectories
            calculate(balls)

            # draw the balls
            for ball in balls:
                screen.blit(ball["img"], ball["pos"])
            
            for text, pos in buttons.items():
                text_surface= font.render(text, True, WHITE)
                rect = text_surface.get_rect(center=pos)
                screen.blit(text_surface, rect)
     
        else:
            # Not animating
            screen.fill(BLACK)
            for text, pos in buttons.items():
                text_surface= font.render(text, True, WHITE)
                rect = text_surface.get_rect(center=pos)
                screen.blit(text_surface, rect)
                
        if time.time() - coord_time < 2:
            text_surface= font.render(coord, True, RED)
            rect = text_surface.get_rect(center=coord_pos)
            screen.blit(text_surface, rect)


        # update the screen
        pygame.display.flip()
 
        # Limit frames per second
        clock.tick(80)

       
except KeyboardInterrupt:
    # clean up GPIO and quit pygame on CTRL+C exit 
    GPIO.cleanup() 
    pygame.quit()

# clean up GPIO and quit pygame on normal exit
GPIO.cleanup() 
pygame.quit()


