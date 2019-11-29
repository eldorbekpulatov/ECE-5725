#!/usr/bin/python2.7
import os
import time
import socket
import random
import subprocess
from constants import IPSTR, BUFFER_SIZE, SERVER_IP, KEY
from multiprocessing import Process, Value, Array, Manager, Pool


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
    soc.bind((SERVER_IP, player.sid)) 
    soc.listen(5) 
    while True: 
        # establish connection with client 
        conn, addr = soc.accept() 
        # data received from client 
        data = eval(conn.recv(BUFFER_SIZE))

        # update teams in parallel
        print(data)
        player.override_teams(data)

        # update the state of the game
        if data["msg"] == "start":
            player.running.value = 1
        elif data["msg"] == "stop":
            player.running.value = 0

        print(data["msg"], player.get_teams())
        
        # send recipt & close
        conn.send(data["msg"]) 
        conn.close()
    soc.close() 


class Player:
    def __init__(self, pub_id):
        self.pid = pub_id
        self.name = "client_"+str(random.randint(0,99))
        self.ip = subprocess.check_output(IPSTR, shell=True).decode("utf-8")[:-1]
        self.manager = Manager()
        self.unassigned = self.manager.dict()
        self.assignedA = self.manager.dict()
        self.assignedB = self.manager.dict()
        self.running = Value("i", 0)
        self.team = None
        self.sid = None
        self.proc = None
        
    def joinRoom(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, self.pid))
            s.send(str({"ip": self.ip, "name" : self.name, "isAlive": 1}))
            self.sid = int(s.recv(BUFFER_SIZE))
            s.close()
        except:
            print("Could NOT establish a Handshake.")
    
    def notifyDeath(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, self.sid))
            s.send(str({"ip": self.ip, "name" :self.name, "isAlive": 0}))
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

    def override_teams(self, data):
        pool = Pool(processes=3)
        pool.apply(overrideDict, args=(self.assignedA, data["assignedA"],))
        pool.apply(overrideDict, args=(self.assignedB, data["assignedB"],))
        pool.apply(overrideDict, args=(self.unassigned, data["unassigned"],))

    def get_teams(self):
        return {"unassigned" : self.unassigned.values(), 
                "assignedA" : self.assignedA.values(), 
                "assignedB" : self.assignedB.values()}



#SERVER_PORT = 3644
#client = Player(SERVER_PORT)
#client.joinRoom()
#client.startListening()
# should get a start mssg
#start_time = time.time()
#while time.time() - start_time < 7:
#    pass
# dies after 7 seconds
#client.notifyDeath()

# client.stopListening()


    
