import os
import sys
import time
import pygame
import subprocess
from pygame.locals import *
import RPi.GPIO as GPIO
from collections import deque

#os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
#os.putenv('SDL_FBDEV', '/dev/fb1')     
#os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

#make mouse invisible
#pygame.mouse.set_visible(False)

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...

pygame.init()

running = True  # Program running
motor_en = True # Motors enabled

# External bailout button
def GPIO27_callback(channel):
    global running
    running = False

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pin 27 - quit 
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)

# Motor Control
# Pin 21 - LLL ==> Left, Clockwise
# Pin 16 - LL  ==> Left, Stop
# Pin 12 - L   ==> Left, Counter-Clockwise
GPIO.setup(21, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(12, GPIO.IN)

# Pin 20 - R   ==> Right, Counter-Clockwise
# Pin 5  - RR  ==> Right, Stop
# Pin 4  - RRR ==> Right, Clockwise
GPIO.setup(20, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(4, GPIO.IN)


#####################SERVOS######################
GPIO.setup(26, GPIO.OUT) # LEFT
GPIO.setup(19, GPIO.OUT) # RIGHT
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # QUIT


def calculateFreqDC(step):
    w = (1.5 + step)
    d = (20+w)
    return (1000/d, w/d*100)

def setMode(step, pwm):
    (fq, dc) = calculateFreqDC(step)    
    pwm.ChangeDutyCycle(dc)      
    pwm.ChangeFrequency(fq)

(fq, dc) = calculateFreqDC(0)                  
pwmL = GPIO.PWM(26, fq)          # Intialize PWM
pwmR = GPIO.PWM(19, fq)          # Intialize PWM

# Motor histories
l_hist = deque([("Stop", 0), ("Stop", 0), ("Stop", 0)])
r_hist = deque([("Stop", 0), ("Stop", 0), ("Stop", 0)])
start_time = time.time()

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
font = pygame.font.Font(None, 20)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
frame_rate = 8
def update_hist(hist, speed):
    hist.pop()
    sec = int(time.time() - start_time)
    if speed > 0:
        hist.appendleft(("Clkwise", sec))
    elif speed < 0:
        hist.appendleft(("Counter-Clk", sec))
    else:
        hist.appendleft(("Stop", sec))
    

def draw_big_button():
    button_surface = pygame.Surface((40,40))
    if motor_en:
        text_surface = font.render("STOP", True, BLACK)
        button_rect = pygame.draw.circle(screen, RED, (95,75), 30)
        text_rect = text_surface.get_rect(center=(160, 120))
    else:
        text_surface = font.render("RESUME", True, BLACK)
        button_rect = pygame.draw.circle(screen, GREEN, (95,75), 30)
        text_rect = text_surface.get_rect(center=(160, 120))
    screen.blit(screen, button_rect)
    screen.blit(text_surface, text_rect)

def draw_histories():
    line_num = 1
    line_spacing = 20
    
    # Left history
    text_surface = font.render("Left History", True, BLACK)
    rect = text_surface.get_rect(midleft=(20, 40))
    screen.blit(text_surface, rect)
    for action, time in l_hist:
        
        # Actions
        text_surface = font.render(action, True, BLACK)
        rect = text_surface.get_rect(midleft=(20, line_num*line_spacing + 80))
        screen.blit(text_surface, rect)
        
        # Times
        text_surface = font.render(str(time), True, BLACK)
        rect = text_surface.get_rect(midright=(120, line_num*line_spacing + 80))
        screen.blit(text_surface, rect)
        
        line_num += 1
    
    line_num = 1
    
    # Right history
    text_surface = font.render("Right History", True, BLACK)
    rect = text_surface.get_rect(midleft=(200, 40))
    screen.blit(text_surface, rect)
    for action, time in r_hist:
        
        # Actions
        text_surface = font.render(action, True, BLACK)
        rect = text_surface.get_rect(midleft=(200, line_num*line_spacing + 80))
        screen.blit(text_surface, rect)
        
        # Times
        text_surface = font.render(str(time), True, BLACK)
        rect = text_surface.get_rect(midright=(300, line_num*line_spacing + 80))
        screen.blit(text_surface, rect)
        
        line_num += 1
        
def draw_quit_button():
    text_surface= font.render("QUIT", True, BLACK)
    rect = text_surface.get_rect(center=(280, 220))
    screen.blit(text_surface, rect)
    
def update_screen():
    screen.fill(WHITE)
    draw_big_button()
    draw_histories()
    draw_quit_button()
    pygame.display.flip()
    
def GPIO21_callback(channel):
    print("falling edge detected on 21")
    speed = -0.2
    update_hist(l_hist, speed)
    update_screen()
    setMode(speed, pwmL)
    

def GPIO16_callback(channel):
    print("falling edge detected on 16")
    speed = 0
    update_hist(l_hist, speed)
    update_screen()
    setMode(speed, pwmL)
    
def GPIO12_callback(channel):
    print("falling edge detected on 12")
    speed = 0.2
    update_hist(l_hist, speed)
    update_screen()
    setMode(speed, pwmL)
    
def GPIO20_callback(channel):
    print("falling edge detected on 20")
    speed = -0.2
    update_hist(r_hist, speed)
    update_screen()
    setMode(speed, pwmR)

def GPIO5_callback(channel):
    print("falling edge detected on 5")
    speed = 0
    update_hist(r_hist, speed)
    update_screen()
    setMode(speed, pwmR)
    
def GPIO4_callback(channel):
    print("falling edge detected on 4")
    speed = 0.2
    update_hist(r_hist, speed)
    update_screen()
    setMode(speed, pwmR)

GPIO.add_event_detect(21, GPIO.FALLING, callback=GPIO21_callback, bouncetime=200)
GPIO.add_event_detect(16, GPIO.FALLING, callback=GPIO16_callback, bouncetime=200)
GPIO.add_event_detect(12, GPIO.FALLING, callback=GPIO12_callback, bouncetime=200)

GPIO.add_event_detect(20, GPIO.FALLING, callback=GPIO20_callback, bouncetime=200)
GPIO.add_event_detect(5, GPIO.FALLING, callback=GPIO5_callback, bouncetime=200)
GPIO.add_event_detect(4, GPIO.FALLING, callback=GPIO4_callback, bouncetime=200)

try: 
    
    pwmL.start(dc)                   # Start PWM
    pwmR.start(dc)                   # Start PWM
    
    # Draw screen
    update_screen()
    
    # ------main loop-------
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif(event.type is MOUSEBUTTONUP):
                x,y = pygame.mouse.get_pos()
                if y < 150 and y > 90 and x < 190 and x > 130:
                    # STOP/RESUME button
                    motor_en = not motor_en
                    if motor_en:
                        # Motors resuming
                        pwmL.start(dc)
                        pwmR.start(dc)
                    else:
                        # Motors stopping
                        pwmL.stop()
                        pwmR.stop()
                    
                    update_screen()
                    
                    
                elif y > 200 and x < 300 and x > 260:
                    # Quit button
                    running = False
       
        # Limit frames per second
        clock.tick(frame_rate)
       
except:
    # turn off pwm, clean up GPIO, and quit pygame on CTRL+C exit 
    pass

# turn off pwm, clean up GPIO, and quit pygame on normal exit
pwmL.stop()
pwmR.stop()
GPIO.cleanup() 
pygame.quit()
