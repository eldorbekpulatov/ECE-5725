import RPi.GPIO as GPIO
import subprocess
import time
import os
import pygame

start = time.time()

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')

playing = True

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pin 27 - quit

def GPIO27_callback(channel):
    global playing
    playing = False
    
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)


###########################################################
#########################PYGAME############################


pygame.init()

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
pygame.display.set_caption("bounce")

path_to_image = "magic_ball.png"

# Starting position of the rectangle
surf_x = 50
surf_y = 50
 
# Speed and direction of rectangle
delta_x = 5
delta_y = 5
    
image = pygame.image.load(path_to_image)


try:
    # -------- Main Program Loop -----------
    while (playing and (time.time() - start < 30)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break
            
        # Set the screen background
        screen.fill(GREEN)
        
        # Draw the ball
        screen.blit(image, (surf_x, surf_y))
        
        # update the screen
        pygame.display.flip()
 
        # Limit to 30 frames per second
        clock.tick(60)
        
        
        # Move the rectangle starting point
        if (surf_x + 128 > width) or (surf_x < 0):
            delta_x = -1*delta_x
        if (surf_y + 128 > height) or (surf_y < 0):
            delta_y = -1*delta_y
    
        surf_x += delta_x
        surf_y += delta_y
        
       
except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
    pygame.quit()

GPIO.cleanup() # clean up GPIO on normal exit
pygame.quit()

