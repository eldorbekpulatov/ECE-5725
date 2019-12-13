import time
import pygame
from pygame.locals import *
import socket
import threading
# import RPi.GPIO as GPIO
import signal
import os
import random
import subprocess
from constants import BUFFER_SIZE, SERVER_IP, KEY
from multiprocessing import Process, Value, Array, Manager, Pool

# Globals
alt = 0
coords = "(0, 0)"
orient = 0
running = True

def overrideDict(sharedStruct, newStruct):
    old_keys = sharedStruct.keys()
    used_keys = []
    for each in newStruct:
        used_keys.append(each[KEY])
        sharedStruct[each[KEY]] = each
    for old_k in old_keys:
        if old_k not in used_keys:
            del sharedStruct[old_k]

def listener(player): 
    soc = socket.socket()   
    soc.bind(("0.0.0.0", player.sid))
    soc.listen(1) 
    print("listening to port ", player.sid)
    while True: 
        # establish connection with client 
        conn, addr = soc.accept() 
        # data received from client 
        data = eval(conn.recv(BUFFER_SIZE).decode("UTF-8"))
        # update teams in parallel
        player.override_teams(data)
        print(data)
        # send recipt 
        conn.send("successfully updated") 
        # close the connection
        conn.close()
        # update the state of the game
        if data["msg"] == "start":
            player.running.value = 1
            print("game started on port ", player.sid)
        elif data["msg"] == "stop":
            player.running.value = 0
            print("game terminated on port ", player.sid)
            break  # exits the loop
    soc.close() 
    print("closed port ", player.sid)

class Player:
    def __init__(self, pub_id):
        self.pid = pub_id
        self.ip = socket.gethostname()
        self.name = "client_"+str(random.randint(0,99))
        self.manager = Manager()
        self.unassigned = self.manager.dict()
        self.assignedA = self.manager.dict()
        self.assignedB = self.manager.dict()
        self.running = Value("i", 0)
        self.isAlive = 1
        self.team = None
        self.sid = None
        self.proc = None
        
    def joinRoom(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, self.pid))
            s.send(str({"ip": self.ip, "name" : self.name, "isAlive": self.isAlive}).encode())
            self.sid = int(s.recv(BUFFER_SIZE).decode("UTF-8"))
            s.close()
            print("joined the game", self.pid)
        except:
            print("Could NOT establish a Handshake.")
    
    def notifyDeath(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, self.sid))
            s.send(str({"ip": self.ip, "name" :self.name, "isAlive": self.isAlive}).encode())
            s.recv(BUFFER_SIZE)
            s.close()
        except:
            print("Could NOT send a death note")

    def startListening(self):
        while not self.proc:
            self.proc = Process(target=listener, args=(self,))
        self.proc.start()

    def stopListening(self):
        while self.proc.is_alive():
            self.proc.terminate()
        self.proc = None

    def override_teams(self, data):
        pool = Pool(processes=3)
        pool.apply(overrideDict, args=(self.assignedA, data["assignedA"],))
        pool.apply(overrideDict, args=(self.assignedB, data["assignedB"],))
        pool.apply(overrideDict, args=(self.unassigned, data["unassigned"],))
        pool.close()
        pool.join()

    def get_teams(self):
        return { "unassigned" : self.unassigned.values(), 
                 "assignedA"  : self.assignedA.values(), 
                 "assignedB"  : self.assignedB.values() }

class UI:
    
    # Screen size
    size = width, height = (320, 240)
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
        
    ### Object coordinates ###
    # quit button
    quit_x = width - 50
    quit_y = 10

    # Center button text for num pad
    num_pad_but_size = 50
    num_pad_but_space = num_pad_but_size + 10
    num_pad_x = [0] * 10
    num_pad_x[1] = 0.5*num_pad_but_space
    num_pad_y = [0] * 10
    num_pad_y[1] = height/2 - 1.5*num_pad_but_space
    for row in range(3):
            for col in range (3):
                num_pad_x[col + row*3 + 1] = num_pad_x[1] + num_pad_but_space*col
                num_pad_y[col + row*3 + 1] = num_pad_y[1] + num_pad_but_space*row
    num_pad_x[0] = num_pad_x[2]
    num_pad_y[0] = num_pad_y[9] + num_pad_but_space
    num_pad_x.append(num_pad_x[1])
    num_pad_x.append(num_pad_x[3])
    num_pad_y.append(num_pad_y[0])
    num_pad_y.append(num_pad_y[0])

    # Center port text for num pad
    port_x = 0.5*(num_pad_x[3] + 0.5*num_pad_but_size + width)
    port_y = height/2-15

    # Team list size
    team_list_size = team_list_width,team_list_height = (width/2,height/2)
    team_list_space = 20

    # Team A list UL
    teamA_x = 0
    teamA_y = 0

    # Team B list UL
    teamB_x = teamA_x
    teamB_y = teamA_y + team_list_height

    # Join team button size
    join_but_size = join_but_width,join_but_height = (80, 40)

    # Join Team A button UL
    joinA_x = 0.5*(teamA_x + team_list_width + width) - 0.5*join_but_width
    joinA_y = height/2 - 50 - 0.5*join_but_height

    # Join Team B button UL
    joinB_x = joinA_x
    joinB_y = joinA_y + 100

    # Button colors for num pad
    num_pad_colors = [BLUE] * 10
    num_pad_colors.append(RED)
    num_pad_colors.append(GREEN)

    def __init__(self):

        #os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
        #os.putenv('SDL_FBDEV', '/dev/fb1')     
        #os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
        #os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

        pygame.init()

        #make mouse invisible
        #pygame.mouse.set_visible(False)

        # window title 
        pygame.display.set_caption("LTA Base Station")# Font and size
        self.font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 30)

        # Set the width and height of the screen [width, height]
        self.screen = pygame.display.set_mode(self.size)
        
        # Game stage
        # 0 - join, 1 - wait for start, 2 - game play, 3 - dead, 4 - game complete
        self.stage = 0
        
        # Port entry
        self.port_txt = ""

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        self.frame_rate = 30
        
        # Error to be printed
        self.print_err = False
        self.err_txt = ''
        self.err_time = time.time()

        # Player team
        # 0 - unassigned, 1 - Team A, 2 - Team B
        self.team = 0

        # Background color
        self.back_color = self.WHITE

        # VestGun object
        self.vest_gun = None
        
    def __draw_quit(self):
        text_surf = self.font.render("QUIT", True, self.WHITE)
        text_rect = text_surf.get_rect(center=(self.quit_x+20,self.quit_y+10))
        button_surf = pygame.Surface((40, 20))
        button_surf.fill(self.RED)
        self.screen.blit(button_surf,(self.quit_x,self.quit_y))
        self.screen.blit(text_surf,text_rect)
        
    def __draw_num_pad(self):

        # Buttons
        for i in range(12):
            txt = ""
            if i == 10:
                txt = "Back"
            elif i == 11:
                txt = "Go"
            else:
                txt = str(i)

            back_surf = pygame.Surface((self.num_pad_but_size,self.num_pad_but_size))
            back_rect = (self.num_pad_x[i] - self.num_pad_but_size/2, self.num_pad_y[i] - self.num_pad_but_size/2)
            back_surf.fill(self.num_pad_colors[i])
            self.screen.blit(back_surf, back_rect)

            txt_surf = self.large_font.render(txt, True, self.WHITE)
            txt_rect = txt_surf.get_rect(center=(self.num_pad_x[i],self.num_pad_y[i]))
            self.screen.blit(txt_surf, txt_rect)

        # Port string
        port_title_surf = self.large_font.render("Game Num", True, self.GREEN)
        port_title_rect = port_title_surf.get_rect(center =(self.port_x, self.port_y))
        self.screen.blit(port_title_surf,port_title_rect)
        port_surf = self.large_font.render(self.port_txt, True, self.YELLOW)
        port_rect = port_surf.get_rect(center = (self.port_x, self.port_y + 30))
        self.screen.blit(port_surf, port_rect)

    def __draw_teams(self,player):

        # Backgrounds
        teamA_back_surf = pygame.Surface(self.team_list_size)
        teamA_back_rect = (self.teamA_x, self.teamA_y)
        teamA_back_surf.fill(self.GREEN)
        self.screen.blit(teamA_back_surf, teamA_back_rect)
        teamB_back_surf = pygame.Surface(self.team_list_size)
        teamB_back_rect = (self.teamB_x, self.teamB_y)
        teamB_back_surf.fill(self.RED)
        self.screen.blit(teamB_back_surf, teamB_back_rect)

        # Titles
        teamA_title_surf = self.font.render("Team A", True, self.WHITE)
        teamA_title_rect = teamA_title_surf.get_rect(topleft =(self.teamA_x, self.teamA_y))
        self.screen.blit(teamA_title_surf,teamA_title_rect)
        teamB_title_surf = self.font.render("Team B", True, self.WHITE)
        teamB_title_rect = teamB_title_surf.get_rect(topleft =(self.teamB_x, self.teamB_y))
        self.screen.blit(teamB_title_surf,teamB_title_rect)

        # teams = player.get_teams()
        teams = { "unassigned" : ["P1", "P2"], 
                 "assignedA"  : ["P3", "P4"], 
                 "assignedB"  : ["P5", "P6"] }
        teamA = teams["assignedA"]
        teamB = teams["assignedB"]
        num_teamA = len(teamA)
        num_teamB = len(teamB)

        # Team sizes
        teamA_size_surf = self.font.render("Members: " + str(num_teamA), True, self.WHITE)
        teamA_size_rect = teamA_title_surf.get_rect(topright =(self.teamA_x + self.team_list_width - 35, self.teamA_y))
        self.screen.blit(teamA_size_surf,teamA_size_rect)
        teamB_size_surf = self.font.render("Members: " + str(num_teamB), True, self.WHITE)
        teamB_size_rect = teamB_title_surf.get_rect(topright =(self.teamB_x + self.team_list_width - 35, self.teamB_y))
        self.screen.blit(teamB_size_surf,teamB_size_rect)

        # Team members
        for memA in range(num_teamA):
            teamA_mem_surf = self.font.render(teamA[memA], True, self.BLACK)
            teamA_mem_rect = teamA_mem_surf.get_rect(topleft =(self.teamA_x, self.teamA_y + (1+memA)*self.team_list_space))
            self.screen.blit(teamA_mem_surf,teamA_mem_rect)
        for memB in range(num_teamB):
            teamB_mem_surf = self.font.render(teamB[memB], True, self.BLACK)
            teamB_mem_rect = teamB_mem_surf.get_rect(topleft =(self.teamB_x, self.teamB_y + (1+memB)*self.team_list_space))
            self.screen.blit(teamB_mem_surf,teamB_mem_rect)

    def __draw_team_select(self):

        # Backgrounds
        joinA_back_surf = pygame.Surface(self.join_but_size)
        joinA_back_rect = (self.joinA_x, self.joinA_y)
        joinA_back_surf.fill(self.GREEN)
        self.screen.blit(joinA_back_surf, joinA_back_rect)
        joinB_back_surf = pygame.Surface(self.join_but_size)
        joinB_back_rect = (self.joinB_x, self.joinB_y)
        joinB_back_surf.fill(self.RED)
        self.screen.blit(joinB_back_surf, joinB_back_rect)

        # Text
        joinA_text_surf = self.large_font.render("Join A", True, self.WHITE)
        joinA_text_rect = joinA_text_surf.get_rect(center=(self.joinA_x + 0.5*self.join_but_width,self.joinA_y + 0.5*self.join_but_height))
        self.screen.blit(joinA_text_surf,joinA_text_rect)
        joinB_text_surf = self.large_font.render("Join B", True, self.WHITE)
        joinB_text_rect = joinB_text_surf.get_rect(center=(self.joinB_x + 0.5*self.join_but_width,self.joinB_y + 0.5*self.join_but_height))
        self.screen.blit(joinB_text_surf,joinB_text_rect)

        # Selection indicator
        if self.team == 1:
            # Team A
            selA_rect = pygame.Rect(self.joinA_x, self.joinA_y, self.join_but_width, self.join_but_height)
            pygame.draw.rect(self.screen, self.YELLOW, selA_rect, 3)
        elif self.team == 2:
            # Team B
            selB_rect = pygame.Rect(self.joinB_x, self.joinB_y, self.join_but_width, self.join_but_height)
            pygame.draw.rect(self.screen, self.YELLOW, selB_rect, 3)
        
    # def __draw_game_info(self):

        
    def __draw_error_running(self):
        if self.print_err:
            if time.time() - self.err_time >= 3:
                # Stop printing error after 3 sec
                self.__print_err = False
            else:
                text_surf = self.font.render(self.err_txt, True, self.RED)
                text_rect = text_surf.get_rect(center=(self.err_x,self.err_y))
                self.screen.blit(text_surf,text_rect)
        
    def wait_frame_rate(self):
        self.clock.tick(self.frame_rate)

    def update_screen(self):
        self.screen.fill(self.back_color)
        self.__draw_quit()
        if self.stage == 0:
            # Port entry stage
            self.__draw_num_pad()
        elif self.stage == 1:
            # Team selection stage
            self.__draw_teams("Player")
            self.__draw_team_select()
        elif self.stage == 2:
            # Game play stage
            pass
        pygame.display.flip()
    
class VestGun:

    def __init__(self,player,laser,trigger,reload,vest,green,red):

        GPIO.setmode(GPIO.BCM)

        # Laser
        GPIO.setup(laser, GPIO.OUT)

        # Trigger
        GPIO.setup(trigger, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(trigger, GPIO.FALLING, callback=self.__trigger_cb, bouncetime=200)
        signal.signal(signal.SIGALRM, __laser_off_cb)
        signal.signal(signal.SIGIALRM, __add_ammo_cb)

        # Reload
        GPIO.setup(reload, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(trigger, GPIO.FALLING, callback=self.__reload_cb, bouncetime=200)
        signal.signal(signal.SIGVTALRM, __add_ammo_cb)

        # Vest sensors
        GPIO.setup(vest, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(trigger, GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)

        # Vest LEDs
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(red, GPIO.OUT)

        self.ammo = 12
        self.health = 100
        self.max_ammo = 12
        self.fire_length = 0.25
        self.reload_interval = 0.1
        self.hit_dmg = 10
        self.alive = True
        self.reloading = False
        self.firing = False
        self.player = player
        self.laser = laser
        self.trigger = trigger
        self.reload = reload
        self.vest = vest
        self.green = green
        self.red = red

    def set_team(self,team):
        if team == 'A':
            GPIO.output(self.green, GPIO.HIGH)
            GPIO.output(self.red, GPIO.LOW)
        elif team == 'B':
            GPIO.output(self.green, GPIO.LOW)
            GPIO.output(self.red, GPIO.HIGH)
        else:
            GPIO.output(self.green, GPIO.LOW)
            GPIO.output(self.red, GPIO.LOW)            

    def __trigger_cb(self):
        # Trigger pressed
        if not self.reloading and not self.firing and self.alive:
            GPIO.output(self.laser, GPIO.HIGH)
            self.firing = True
            signal.setitimer(signal.ITIMER_REAL, self.fire_length)

    def __laser_off_cb(self):
        # Turning laser off
        GPIO.output(self.laser, GPIO.LOW)
        self.firing = False

    def __reload_cb(self):
        # Reloading button pressed
        if not self.reloading and not self.firing and self.ammo < self.max_ammo and self.alive:
            self.reloading = True
            signal.setitimer(signal.ITIMER_VIRTUAL, self.reload_interval)

    def __add_ammo_cb(self):
        # Add one to ammo
        self.ammo += 1
        if self.ammo < self.max_ammo and self.alive:
            signal.setitimer(signal.ITIMER_VIRTUAL, self.reload_interval)

    def __hit_cb(self):
        # Hit detected on vest
        if self.alive:
            self.health -= self.hit_dmg
            if self.health <= 0:
                # dead
                self.alive = False
                self.player.notifyDeath()
    

if __name__ == '__main__':
    
    try:

        ui = UI()
        ui.update_screen()

        while running:

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    elif(event.type is MOUSEBUTTONDOWN):
                        # Mouse click
                        x,y = pygame.mouse.get_pos()

                        if x > ui.quit_x and x < ui.quit_x + 40 and y < ui.quit_y + 20 and y > ui.quit_y:
                            # Quit button clicked
                            running = False
                            # terminate_server(server_ip,server_port)
                        elif ui.stage == 0:
                            # Entering port
                            for i in range(12):
                                if x > ui.num_pad_x[i] - ui.num_pad_but_size/2 and x < ui.num_pad_x[i] + ui.num_pad_but_size/2 \
                                    and y > ui.num_pad_y[i] - ui.num_pad_but_size/2 and y < ui.num_pad_y[i] + ui.num_pad_but_size/2:
                                    if i < 10:
                                        # Number button
                                        ui.port_txt += str(i)
                                    elif i == 10:
                                        # Back button
                                        ui.port_txt = ui.port_txt[:-1]
                                    else:
                                        # Go button
                                        # game = Player(int(ui.port_txt))
                                        # game.joinRoom()
                                        # game.startListening()
                                        ui.port_txt = ""
                                        ui.stage = 1
                                        pass
                        elif ui.stage == 1:
                            # Waiting for game start
                            if x > ui.joinA_x and x < ui.joinA_x + ui.join_but_width and y > ui.joinA_y and y < ui.joinA_y + ui.join_but_height:
                                # Join A button
                                ui.team = 1
                            elif x > ui.joinB_x and x < ui.joinB_x + ui.join_but_width and y > ui.joinB_y and y < ui.joinB_y + ui.join_but_height:
                                # Join B button
                                ui.team = 2
                        elif ui.stage == 2:
                            # Game play
                            pass
                        elif ui.stage == 3:
                            # Death
                            pass
            
            ui.update_screen()
            ui.wait_frame_rate()
    except:
        print("Error")
        #terminate_server(server_ip,server_port)
        pygame.quit()
        raise
    
    #terminate_server(server_ip,server_port)
    pygame.quit()

