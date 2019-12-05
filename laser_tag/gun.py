import time
import pygame
from pygame.locals import *
import socket
import threading

# Globals
alt = 0
coords = "(0, 0)"
orient = 0
running = True

class conn():
    
    def __init__(self, ip, port):
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientSocket.connect((ip,port))
    
    def get_coord(self):
        self.clientSocket.send("coord".encode())
        msg, addr = self.clientSocket.recvfrom(1024)
        #return tuple(map(int,msg.decode().split(',')))
        return msg.decode()
    
    def get_alt(self):
        self.clientSocket.send("alt".encode())
        msg, addr = self.clientSocket.recvfrom(1024)
        return msg.decode()
        
    def get_orient(self):
        self.clientSocket.send("orient".encode())
        msg, addr = self.clientSocket.recvfrom(1024)
        return msg.decode()
        
    def get_wp(self):
        self.clientSocket.send("curr wp".encode())
        msg,addr = self.clientSocket.recvfrom(1024)
        return msg.decode()
        
    def send_acc(self, dir):
        if dir == "forward" or dir == "backward" or dir == "right" \
            or dir == "left" or dir == "up" or dir == "down" or dir == "stop":
            self.clientSocket.send(dir.encode())
        else:
            raise Exception("Acceleration direction not recognized")
            
    def send_wp(self, x, y, z, theta):
        str = "wp " + x + "," + y + "," + z + "," + theta
        self.clientSocket.send(str.encode())
        
    def send_drive(self,mode):
        str = "mode " + mode
        self.clientSocket.send(str.encode())
    
    def exit(self):
        self.clientSocket.send("quit".encode())
        self.clientSocket.recvfrom(1024)
    
    def close(self):
        self.clientSocket.close()

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


    # Button colors for num pad
    num_pad_colors = [BLUE] * 10
    num_pad_colors.append(RED)
    num_pad_colors.append(GREEN)
        
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
        self.screen.fill(self.WHITE)
        self.__draw_quit()
        if self.stage == 0:
            # Port entry stage
            self.__draw_num_pad()
        pygame.display.flip()

    def __init__(self):
        pygame.init()

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
    
def terminate_server(ip,port):
    server = conn(ip,port)
    server.exit()
    server.close()
    

if __name__ == '__main__':
    
    try:
        server_ip = 'localhost'

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
                                        # open port connection
                                        ui.port_txt = ""
                                        ui.stage = 1
                                        pass
                        elif ui.stage == 1:
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

